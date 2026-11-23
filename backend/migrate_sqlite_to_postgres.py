"""Copy local SQLite enquiries and notification state into PostgreSQL."""

import sqlite3
import sys

from feast_api import database
from feast_api.config import DATABASE_URL, DB_PATH


def main():
    if not DATABASE_URL:
        raise SystemExit("Set DATABASE_URL in the project .env before migrating.")

    database.initialize_database(DB_PATH)
    database.initialize_database(DATABASE_URL)

    with sqlite3.connect(DB_PATH) as source:
        source.row_factory = sqlite3.Row
        quotes = [dict(row) for row in source.execute("SELECT * FROM quotes")]
        notifications = [dict(row) for row in source.execute("SELECT * FROM notification_outbox")]

    with database.connect_database(DATABASE_URL) as target:
        for quote in quotes:
            target.execute(
                """INSERT INTO quotes(id,event_type,event_date,guests,name,email,notes,status,created_at)
                   VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING""",
                tuple(quote[field] for field in (
                    "id", "event_type", "event_date", "guests", "name", "email", "notes", "status", "created_at"
                )),
            )
        for item in notifications:
            target.execute(
                """INSERT INTO notification_outbox(id,quote_id,created_at,attempts,next_attempt_at,sent_at,last_error)
                   VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING""",
                tuple(item[field] for field in (
                    "id", "quote_id", "created_at", "attempts", "next_attempt_at", "sent_at", "last_error"
                )),
            )
        target.execute(
            "SELECT setval(pg_get_serial_sequence('quotes','id'), COALESCE(MAX(id),1), MAX(id) IS NOT NULL) FROM quotes"
        )
        target.execute(
            "SELECT setval(pg_get_serial_sequence('notification_outbox','id'), COALESCE(MAX(id),1), MAX(id) IS NOT NULL) FROM notification_outbox"
        )

    print(f"Migrated {len(quotes)} quote(s) and {len(notifications)} notification record(s).")


if __name__ == "__main__":
    try:
        main()
    except (sqlite3.Error, RuntimeError) as error:
        print(f"Migration failed: {error}", file=sys.stderr)
        raise SystemExit(1) from None
