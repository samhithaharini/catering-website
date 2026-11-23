import asyncio
import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from . import database
from .config import logger


class QuoteStorageError(Exception):
    """Raised when a quote cannot be saved to persistent storage."""


class QuoteService:
    """Quote persistence and notification delivery."""

    def __init__(self, db_path):
        self.db_path = db_path

    def create_quote(self, payload):
        timestamp = datetime.now(timezone.utc).isoformat()
        try:
            with database.connect_database(self.db_path) as connection:
                cursor = connection.execute(
                    ("""INSERT INTO quotes(event_type,event_date,guests,name,email,notes,created_at)
                       VALUES(?,?,?,?,?,?,?) RETURNING id""" if database.is_postgres(self.db_path) else
                     """INSERT INTO quotes(event_type,event_date,guests,name,email,notes,created_at)
                       VALUES(?,?,?,?,?,?,?)"""),
                    (payload.event_type, payload.event_date.isoformat(), payload.guests,
                     payload.name, payload.email, payload.notes, timestamp),
                )
                quote_id = cursor.fetchone()["id"] if database.is_postgres(self.db_path) else cursor.lastrowid
                connection.execute(
                    "INSERT INTO notification_outbox(quote_id,created_at,next_attempt_at) VALUES(?,?,?)",
                    (quote_id, timestamp, timestamp),
                )
            return quote_id
        except Exception as error:
            if not database.is_database_error(error):
                raise
            logger.exception("Could not save quote request")
            raise QuoteStorageError from error

    @staticmethod
    def smtp_settings():
        host = os.environ.get("FEAST_SMTP_HOST", "").strip()
        recipient = os.environ.get("FEAST_NOTIFICATION_TO", "").strip()
        sender = os.environ.get("FEAST_NOTIFICATION_FROM", "").strip()
        if not host or not recipient or not sender:
            return None
        return {
            "host": host,
            "port": int(os.environ.get("FEAST_SMTP_PORT", "587")),
            "user": os.environ.get("FEAST_SMTP_USER", ""),
            "password": os.environ.get("FEAST_SMTP_PASSWORD", ""),
            "recipient": recipient,
            "sender": sender,
            "starttls": os.environ.get("FEAST_SMTP_STARTTLS", "true").lower() == "true",
            "ssl": os.environ.get("FEAST_SMTP_SSL", "false").lower() == "true",
        }

    @staticmethod
    def deliver_notification(settings, quote):
        message = EmailMessage()
        message["Subject"] = f"New Amutham enquiry #{quote['id']} — {quote['event_type']}"
        message["From"] = settings["sender"]
        message["To"] = settings["recipient"]
        message.set_content(
            f"A new catering enquiry was received.\n\n"
            f"Request: #{quote['id']}\nEvent: {quote['event_type']}\nDate: {quote['event_date']}\n"
            f"Guests: {quote['guests']}\nName: {quote['name']}\nEmail: {quote['email']}\n\n"
            f"Notes:\n{quote['notes'] or '(none)'}\n"
        )
        smtp_client = smtplib.SMTP_SSL if settings["ssl"] else smtplib.SMTP
        with smtp_client(settings["host"], settings["port"], timeout=15) as smtp:
            if settings["starttls"] and not settings["ssl"]:
                smtp.starttls()
            if settings["user"]:
                smtp.login(settings["user"], settings["password"])
            smtp.send_message(message)

    def send_notification_for_quote(self, quote_id):
        """Send the newly saved enquiry before a serverless request returns."""
        settings = self.smtp_settings()
        if not settings:
            return False
        with database.connect_database(self.db_path) as connection:
            row = connection.execute(
                """SELECT o.id AS outbox_id, o.attempts, q.* FROM notification_outbox o
                   JOIN quotes q ON q.id=o.quote_id
                   WHERE q.id=? AND o.sent_at IS NULL""",
                (quote_id,),
            ).fetchone()
        if not row:
            return False
        return self._deliver_outbox_record(settings, dict(row))

    def _deliver_outbox_record(self, settings, quote):
        try:
            self.deliver_notification(settings, quote)
            with database.connect_database(self.db_path) as connection:
                connection.execute(
                    "UPDATE notification_outbox SET sent_at=?, attempts=attempts+1, last_error=NULL WHERE id=?",
                    (datetime.now(timezone.utc).isoformat(), quote["outbox_id"]),
                )
            return True
        except Exception as error:
            attempts = quote["attempts"] + 1
            delay = min(3600, 30 * (2 ** min(attempts - 1, 7)))
            with database.connect_database(self.db_path) as connection:
                connection.execute(
                    "UPDATE notification_outbox SET attempts=?, next_attempt_at=?, last_error=? WHERE id=?",
                    (attempts, (datetime.now(timezone.utc) + timedelta(seconds=delay)).isoformat(),
                     str(error)[:500], quote["outbox_id"]),
                )
            logger.exception("Notification delivery failed for quote %s", quote["id"])
            return False

    def process_pending_notifications(self, limit=25):
        settings = self.smtp_settings()
        if not settings:
            return 0
        now = datetime.now(timezone.utc).isoformat()
        with database.connect_database(self.db_path) as connection:
            rows = connection.execute(
                """SELECT o.id AS outbox_id, o.attempts, q.* FROM notification_outbox o
                   JOIN quotes q ON q.id=o.quote_id
                   WHERE o.sent_at IS NULL AND o.next_attempt_at <= ?
                   ORDER BY o.id LIMIT ?""",
                (now, limit),
            ).fetchall()
        for row in rows:
            self._deliver_outbox_record(settings, dict(row))
        return len(rows)

    def _pending_notification(self):
        now = datetime.now(timezone.utc).isoformat()
        with database.connect_database(self.db_path) as connection:
            return connection.execute(
                """SELECT o.id AS outbox_id, q.* FROM notification_outbox o
                   JOIN quotes q ON q.id=o.quote_id
                   WHERE o.sent_at IS NULL AND o.next_attempt_at <= ?
                   ORDER BY o.id LIMIT 1""",
                (now,),
            ).fetchone()

    async def notification_worker(self):
        while True:
            try:
                settings = self.smtp_settings()
                pending = self._pending_notification() if settings else None
                if pending:
                    quote = dict(pending)
                    try:
                        await asyncio.to_thread(self.deliver_notification, settings, quote)
                        with database.connect_database(self.db_path) as connection:
                            connection.execute(
                                "UPDATE notification_outbox SET sent_at=?, attempts=attempts+1, last_error=NULL WHERE id=?",
                                (datetime.now(timezone.utc).isoformat(), quote["outbox_id"]),
                            )
                    except Exception as error:  # Keep the quote; retry notification with bounded backoff.
                        with database.connect_database(self.db_path) as connection:
                            row = connection.execute(
                                "SELECT attempts FROM notification_outbox WHERE id=?", (quote["outbox_id"],)
                            ).fetchone()
                            stored_attempts = (row["attempts"] if isinstance(row, dict) else row[0]) if row else 0
                            attempts = stored_attempts + 1
                            delay = min(3600, 30 * (2 ** min(attempts - 1, 7)))
                            connection.execute(
                                "UPDATE notification_outbox SET attempts=?, next_attempt_at=?, last_error=? WHERE id=?",
                                (attempts, (datetime.now(timezone.utc) + timedelta(seconds=delay)).isoformat(),
                                 str(error)[:500], quote["outbox_id"]),
                            )
                        logger.exception("Notification delivery failed for quote %s", quote["id"])
                await asyncio.sleep(2 if pending else 30)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Notification worker encountered an error")
                await asyncio.sleep(30)
