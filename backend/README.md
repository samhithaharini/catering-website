# Amutham backend

The backend is split by responsibility in `feast_api/`:

- `config.py` contains environment-backed settings and shared constants.
- `models.py` defines the database record model returned by services.
- `schemas.py` validates incoming API data.
- `database.py` owns SQLite/PostgreSQL connections, versioned schema migrations, and local SQLite backups.
- `services.py` implements quote persistence, SMTP delivery, and retries.
- `router.py` defines the public quote submission endpoint.
- `middleware.py` applies request-size limits, rate limits, request IDs, and request logging.
- `main.py` assembles the FastAPI application and manages startup/shutdown.
- `server.py` remains the local CLI entry point for running the server and database maintenance.
- `migrate_sqlite_to_postgres.py` copies local SQLite enquiries into the configured PostgreSQL database.

From this directory, install dependencies and run the API:

```powershell
py -m pip install -r requirements.txt
py server.py
```

Local runs use SQLite unless `DATABASE_URL` is set. Production deployments
should set `DATABASE_URL` to the pooled PostgreSQL connection string. Set
`DATABASE_URL_UNPOOLED` to the direct connection string for schema migrations;
the app uses the pooled URL for regular enquiry operations.

