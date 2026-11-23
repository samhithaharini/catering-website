import re
from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import EVENT_TYPES


class QuoteInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: str
    event_date: date
    guests: int = Field(strict=True, ge=1, le=10_000)
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=254)
    notes: str = Field(default="", max_length=2_000)
    website: str = Field(default="", max_length=500)  # Honeypot; real visitors leave this empty.

    @field_validator("event_type")
    @classmethod
    def check_event_type(cls, value):
        value = value.strip()
        if value not in EVENT_TYPES:
            raise ValueError("Please select a valid event type.")
        return value

    @field_validator("name", "email", "notes")
    @classmethod
    def trim_text(cls, value):
        return value.strip()

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        if not value:
            raise ValueError("Name is required.")
        return value

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            raise ValueError("Please provide a valid email address.")
        return value


