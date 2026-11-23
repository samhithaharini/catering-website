import logging
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ENV = BASE_DIR.parent / ".env"


def _load_project_env():
    """Load simple KEY=VALUE entries for local runs; shell environment wins."""
    if not PROJECT_ENV.is_file():
        return
    for raw_line in PROJECT_ENV.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, separator, value = line.partition("=")
        key = key.strip()
        if not separator or not key or not key.replace("_", "").isalnum() or key[0].isdigit() or key in os.environ:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        else:
            value = value.split(" #", 1)[0].strip()
        os.environ[key] = value


_load_project_env()

DB_PATH = Path(os.environ.get("FEAST_DB_PATH", BASE_DIR / "data" / "quotes.db")).resolve()
DATABASE_URL = os.environ.get("DATABASE_URL", os.environ.get("FEAST_DATABASE_URL", "")).strip()
DATABASE_URL_UNPOOLED = os.environ.get("DATABASE_URL_UNPOOLED", "").strip()
HOST = os.environ.get("FEAST_HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", os.environ.get("FEAST_PORT", "8000")))
CORS_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in os.environ.get("FEAST_CORS_ORIGINS", "").split(",")
    if origin.strip()
]
IS_VERCEL = os.environ.get("VERCEL") == "1"
CRON_SECRET = os.environ.get("CRON_SECRET", "")
MAX_BODY_SIZE = 16_384
RATE_LIMIT = int(os.environ.get("FEAST_RATE_LIMIT", "10"))
RATE_WINDOW_SECONDS = int(os.environ.get("FEAST_RATE_WINDOW_SECONDS", "60"))
EVENT_TYPES = {"wedding", "corporate", "private-party", "cocktail", "buffet", "plated"}
logger = logging.getLogger("amutham.api")
