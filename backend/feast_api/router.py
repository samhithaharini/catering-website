import hmac

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

from . import config
from .schemas import QuoteInput
from .services import QuoteService, QuoteStorageError


def create_router(service: QuoteService):
    router = APIRouter()

    @router.get("/api/cron/notifications")
    def retry_notifications(authorization: str | None = Header(default=None)):
        expected = f"Bearer {config.CRON_SECRET}" if config.CRON_SECRET else ""
        if not expected or not hmac.compare_digest(authorization or "", expected):
            raise HTTPException(status_code=401, detail="Not authorized.")
        return {"processed": service.process_pending_notifications()}

    @router.get("/api/quotes")
    def quotes_get():
        raise HTTPException(status_code=405, detail="Use POST to submit a quote request.", headers={"Allow": "POST"})

    @router.post("/api/quotes", status_code=201)
    def create_quote(payload: QuoteInput):
        if payload.website:
            return JSONResponse({"accepted": True}, status_code=202)
        try:
            quote_id = service.create_quote(payload)
            if config.IS_VERCEL:
                service.send_notification_for_quote(quote_id)
        except QuoteStorageError:
            raise HTTPException(status_code=500, detail="The enquiry could not be saved. Please try again.") from None
        return {"id": quote_id, "accepted": True}

    return router
