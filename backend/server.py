"""Command-line entry point for the Amutham API and database maintenance."""

import argparse

from feast_api import database
from feast_api.config import DATABASE_URL, DB_PATH
from feast_api.main import app, create_app, run_server


def main():
    parser = argparse.ArgumentParser(description="Amutham quote API and database maintenance")
    parser.add_argument("--backup", action="store_true", help="Create a consistent SQLite backup and exit")
    parser.add_argument("--purge-older-than-days", type=int, help="Back up, then delete older quote records")
    args = parser.parse_args()
    if args.backup:
        print(database.backup_database())
        return
    if args.purge_older_than_days is not None:
        count, backup = database.purge_old_quotes(DATABASE_URL or DB_PATH, args.purge_older_than_days)
        print(f"Deleted {count} quote(s). Backup: {backup}")
        return
    run_server()


if __name__ == "__main__":
    main()
