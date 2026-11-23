import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import config, database
from .middleware import RequestSizeLimitMiddleware, install_request_controls
from .router import create_router
from .services import QuoteService


def _validation_error_handler(_request, error):
    first = error.errors()[0]
    field = first.get("loc", (None,))[-1]
    if field == "guests":
        message = "Guest count must be between 1 and 10,000."
    else:
        message = first.get("msg", "Please check the submitted fields.").removeprefix("Value error, ")
    return JSONResponse({"error": message}, status_code=400)


def create_app(db_path=None):
    if config.IS_VERCEL and not (db_path or config.DATABASE_URL):
        raise RuntimeError("DATABASE_URL must point to PostgreSQL when running on Vercel.")
    target_db = db_path or config.DATABASE_URL or config.DB_PATH
    quote_service = QuoteService(target_db)

    @asynccontextmanager
    async def lifespan(_app):
        migration_db = db_path or (
            config.DATABASE_URL_UNPOOLED
            if database.is_postgres(target_db) and config.DATABASE_URL_UNPOOLED
            else target_db
        )
        database.initialize_database(migration_db)
        if not QuoteService.smtp_settings():
            config.logger.warning("Email notifications are not configured; quote requests will only be saved to the database.")
        worker = None if config.IS_VERCEL else asyncio.create_task(quote_service.notification_worker())
        try:
            yield
        finally:
            if worker:
                worker.cancel()
                try:
                    await worker
                except asyncio.CancelledError:
                    pass

    application = FastAPI(
        title="Amutham Quote API",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )
    install_request_controls(application)
    application.add_middleware(RequestSizeLimitMiddleware)
    if config.CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=config.CORS_ORIGINS,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Content-Type"],
        )
    application.add_exception_handler(RequestValidationError, _validation_error_handler)
    application.include_router(create_router(quote_service))

    @application.get("/health")
    def health():
        return {"status": "ok"}

    return application


app = create_app()


def run_server():
    logging.basicConfig(level=os.environ.get("FEAST_LOG_LEVEL", "INFO"), stream=sys.stdout)
    import uvicorn

    uvicorn.run(
        "server:app", host=config.HOST, port=config.PORT, workers=1, proxy_headers=True,
        forwarded_allow_ips=os.environ.get("FEAST_TRUSTED_PROXIES", "127.0.0.1"),
    )
