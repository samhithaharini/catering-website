import json
import re
import time
from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse

from . import config


class RequestBodyTooLarge(Exception):
    pass


class RequestSizeLimitMiddleware:
    """Enforce the quote request cap while streaming, including chunked requests."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("path") != "/api/quotes" or scope.get("method") != "POST":
            await self.app(scope, receive, send)
            return
        headers = {key.lower(): value for key, value in scope.get("headers", [])}
        raw_length = headers.get(b"content-length")
        if raw_length:
            try:
                if int(raw_length) > config.MAX_BODY_SIZE:
                    await self._response(send, 413, {"error": "Request must be 16 KB or smaller."})
                    return
            except ValueError:
                await self._response(send, 400, {"error": "Invalid request size."})
                return

        consumed = 0

        async def receive_limited():
            nonlocal consumed
            message = await receive()
            if message["type"] == "http.request":
                consumed += len(message.get("body", b""))
                if consumed > config.MAX_BODY_SIZE:
                    raise RequestBodyTooLarge
            return message

        try:
            await self.app(scope, receive_limited, send)
        except RequestBodyTooLarge:
            await self._response(send, 413, {"error": "Request must be 16 KB or smaller."})

    @staticmethod
    async def _response(send, status, payload):
        body = json.dumps(payload).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())],
        })
        await send({"type": "http.response.body", "body": body})


def install_request_controls(application):
    rate_hits = {}

    @application.middleware("http")
    async def request_controls(request: Request, call_next):
        started = time.monotonic()
        supplied_request_id = request.headers.get("X-Request-ID", "")
        request_id = supplied_request_id if re.fullmatch(r"[A-Za-z0-9._-]{1,80}", supplied_request_id) else str(uuid4())

        def log_early_response(response):
            response.headers["X-Request-ID"] = request_id
            _log_request(request, response.status_code, started, request_id)
            return response

        is_quote_submit = request.url.path == "/api/quotes" and request.method == "POST"
        if is_quote_submit:
            content_type = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()
            if content_type != "application/json":
                return log_early_response(JSONResponse({"error": "Send the request as JSON."}, status_code=415))
        if is_quote_submit:
            host = request.client.host if request.client else "unknown"
            now = time.monotonic()
            key = f"{host}:quote"
            limit = config.RATE_LIMIT
            recent = [stamp for stamp in rate_hits.get(key, []) if now - stamp < config.RATE_WINDOW_SECONDS]
            if len(recent) >= limit:
                response = JSONResponse({"error": "Too many enquiries. Please try again later."}, status_code=429)
                response.headers["Retry-After"] = str(config.RATE_WINDOW_SECONDS)
                return log_early_response(response)
            recent.append(now)
            rate_hits[key] = recent
            if len(rate_hits) > 10_000:
                rate_hits.clear()

        try:
            response = await call_next(request)
        except Exception:
            config.logger.exception("Unhandled API error request_id=%s", request_id)
            response = JSONResponse({"error": "The request could not be completed."}, status_code=500)
        response.headers["X-Request-ID"] = request_id
        _log_request(request, response.status_code, started, request_id)
        return response


def _log_request(request, status, started, request_id):
    config.logger.info(
        "request_id=%s method=%s path=%s status=%s elapsed_ms=%d client=%s",
        request_id, request.method, request.url.path, status,
        int((time.monotonic() - started) * 1000), request.client.host if request.client else "unknown",
    )
