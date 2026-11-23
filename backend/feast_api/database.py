import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .config import DATABASE_URL, DB_PATH


def is_postgres(db_path=None):
    target = str(db_path or DATABASE_URL)
    return target.startswith(("postgres://", "postgresql://"))


def is_database_error(error):
    return isinstance(error, sqlite3.Error) or error.__class__.__module__.startswith("psycopg")


class _PostgresConnection:
    """Small adapter that keeps service SQL parameters portable."""

    def __init__(self, connection):
        self.connection = connection

    def execute(self, statement, parameters=()):
        return self.connection.execute(statement.replace("?", "%s"), parameters)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()

    def __enter__(self):
        self.connection.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.connection.__exit__(exc_type, exc_value, traceback)


def connect_database(db_path=None):
    if is_postgres(db_path):
        import psycopg
        from psycopg.rows import dict_row

        return _PostgresConnection(psycopg.connect(
            str(db_path or DATABASE_URL), row_factory=dict_row, connect_timeout=10
        ))
    path = Path(db_path or DB_PATH).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        path.parent.chmod(0o700)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = NORMAL")
    return connection


def backup_database(db_path=None, destination=None):
    if is_postgres(db_path or DATABASE_URL):
        raise RuntimeError("Use the PostgreSQL provider's backup tools for PostgreSQL databases.")
    source_path = Path(db_path or DB_PATH).resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"Database does not exist: {source_path}")
    backup_path = Path(destination).resolve() if destination else source_path.with_name(
        f"{source_path.stem}-backup-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}{source_path.suffix}"
    )
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(source_path) as source, sqlite3.connect(backup_path) as target:
        source.backup(target)
    if os.name != "nt":
        backup_path.chmod(0o600)
    return backup_path


def _table_exists(connection, table):
    return connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone() is not None


def _create_quotes_table(connection):
    connection.execute(
        """CREATE TABLE quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL CHECK(event_type IN ('wedding','corporate','private-party','cocktail','buffet','plated')),
            event_date TEXT NOT NULL CHECK(length(event_date) = 10),
            guests INTEGER NOT NULL CHECK(guests BETWEEN 1 AND 10000),
            name TEXT NOT NULL CHECK(length(trim(name)) BETWEEN 1 AND 120),
            email TEXT NOT NULL CHECK(length(email) BETWEEN 3 AND 254),
            notes TEXT NOT NULL DEFAULT '' CHECK(length(notes) <= 2000),
            status TEXT NOT NULL DEFAULT 'new' CHECK(status IN ('new','contacted','booked','declined')),
            created_at TEXT NOT NULL
        )"""
    )


def _migration_one(connection):
    """Create the constrained quote table and preserve rows from the original schema."""
    previous_columns = set()
    if _table_exists(connection, "quotes"):
        previous_columns = {row[1] for row in connection.execute("PRAGMA table_info(quotes)")}
        connection.execute("ALTER TABLE quotes RENAME TO quotes_before_migration")
    _create_quotes_table(connection)
    if previous_columns:
        available = {
            "id": "id",
            "event_type": "event_type",
            "event_date": "event_date",
            "guests": "guests",
            "name": "name",
            "email": "email",
            "notes": "notes" if "notes" in previous_columns else "''",
            "status": "status" if "status" in previous_columns else "'new'",
            "created_at": "created_at" if "created_at" in previous_columns else "CURRENT_TIMESTAMP",
        }
        required = {"event_type", "event_date", "guests", "name", "email"}
        if not required.issubset(previous_columns):
            raise RuntimeError("Existing quote table is missing required columns; preserve a backup and migrate it manually.")
        columns = list(available)
        connection.execute(
            f"INSERT INTO quotes ({', '.join(columns)}) SELECT {', '.join(available[c] for c in columns)} FROM quotes_before_migration"
        )
        connection.execute("DROP TABLE quotes_before_migration")
    connection.execute("CREATE INDEX quotes_created_at_idx ON quotes(created_at DESC)")
    connection.execute("CREATE INDEX quotes_status_idx ON quotes(status, created_at DESC)")


def _migration_two(connection):
    connection.execute(
        """CREATE TABLE notification_outbox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_id INTEGER NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
            created_at TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0 CHECK(attempts >= 0),
            next_attempt_at TEXT NOT NULL,
            sent_at TEXT,
            last_error TEXT
        )"""
    )
    connection.execute("CREATE INDEX notification_pending_idx ON notification_outbox(sent_at, next_attempt_at)")


MIGRATIONS = [(1, _migration_one), (2, _migration_two)]


def _postgres_migration_one(connection):
    connection.execute(
        """CREATE TABLE IF NOT EXISTS quotes (
            id BIGSERIAL PRIMARY KEY,
            event_type TEXT NOT NULL CHECK(event_type IN ('wedding','corporate','private-party','cocktail','buffet','plated')),
            event_date TEXT NOT NULL CHECK(length(event_date) = 10),
            guests INTEGER NOT NULL CHECK(guests BETWEEN 1 AND 10000),
            name TEXT NOT NULL CHECK(length(trim(name)) BETWEEN 1 AND 120),
            email TEXT NOT NULL CHECK(length(email) BETWEEN 3 AND 254),
            notes TEXT NOT NULL DEFAULT '' CHECK(length(notes) <= 2000),
            status TEXT NOT NULL DEFAULT 'new' CHECK(status IN ('new','contacted','booked','declined')),
            created_at TEXT NOT NULL
        )"""
    )
    connection.execute("CREATE INDEX IF NOT EXISTS quotes_created_at_idx ON quotes(created_at DESC)")
    connection.execute("CREATE INDEX IF NOT EXISTS quotes_status_idx ON quotes(status, created_at DESC)")


def _postgres_migration_two(connection):
    connection.execute(
        """CREATE TABLE IF NOT EXISTS notification_outbox (
            id BIGSERIAL PRIMARY KEY,
            quote_id BIGINT NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
            created_at TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0 CHECK(attempts >= 0),
            next_attempt_at TEXT NOT NULL,
            sent_at TEXT,
            last_error TEXT
        )"""
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS notification_pending_idx ON notification_outbox(sent_at, next_attempt_at)"
    )


POSTGRES_MIGRATIONS = [(1, _postgres_migration_one), (2, _postgres_migration_two)]


def _initialize_postgres_database(database_url):
    with connect_database(database_url) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"
        )
        connection.execute("SELECT pg_advisory_xact_lock(?)", (7_414_220_026,))
        applied = {row["version"] for row in connection.execute("SELECT version FROM schema_migrations").fetchall()}
        for version, migrate in POSTGRES_MIGRATIONS:
            if version in applied:
                continue
            migrate(connection)
            connection.execute(
                "INSERT INTO schema_migrations(version, applied_at) VALUES (?, ?)",
                (version, datetime.now(timezone.utc).isoformat()),
            )


def initialize_database(db_path=None):
    target = db_path or DATABASE_URL or DB_PATH
    if is_postgres(target):
        _initialize_postgres_database(str(target))
        return
    path = Path(target).resolve()
    existed = path.exists() and path.stat().st_size > 0
    needs_backup = False
    if existed:
        with sqlite3.connect(path) as existing:
            tables = {row[0] for row in existing.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "quotes" in tables:
                versions = set()
                if "schema_migrations" in tables:
                    versions = {row[0] for row in existing.execute("SELECT version FROM schema_migrations")}
                needs_backup = any(version not in versions for version, _ in MIGRATIONS)
    if needs_backup:
        backup_database(path)
    connection = connect_database(path)
    try:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"
        )
        applied = {row[0] for row in connection.execute("SELECT version FROM schema_migrations")}
        for version, migrate in MIGRATIONS:
            if version in applied:
                continue
            connection.execute("BEGIN IMMEDIATE")
            try:
                migrate(connection)
                connection.execute(
                    "INSERT INTO schema_migrations(version, applied_at) VALUES (?, ?)",
                    (version, datetime.now(timezone.utc).isoformat()),
                )
                connection.commit()
            except Exception:
                connection.rollback()
                raise
        if os.name != "nt":
            path.chmod(0o600)
    finally:
        connection.close()


def purge_old_quotes(db_path, older_than_days):
    if older_than_days < 1:
        raise ValueError("Retention must be at least one day.")
    target = db_path or DATABASE_URL or DB_PATH
    if is_postgres(target):
        raise RuntimeError("Use the PostgreSQL provider's backup and retention tools for PostgreSQL databases.")
    backup = backup_database(target)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=older_than_days)).isoformat()
    with connect_database(target) as connection:
        cursor = connection.execute("DELETE FROM quotes WHERE created_at < ?", (cutoff,))
    return cursor.rowcount, backup
