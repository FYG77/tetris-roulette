from __future__ import annotations

import functools
import os
from typing import Any

from pydantic import BaseModel, Field


class StripeSettings(BaseModel):
    secret_key: str = Field(default="")
    price_5: str = Field(default="")
    price_10: str = Field(default="")
    price_20: str = Field(default="")


class Settings(BaseModel):
    mongo_uri: str = Field(default="mongodb://mongo:27017/tetris")
    jwt_secret: str = Field(default="change_me")
    port: int = Field(default=8000)
    rake_percent: int = Field(default=10)
    queue_timeout_ms: int = Field(default=15000)
    match_duration_ms: int = Field(default=60000)
    min_stake: int = Field(default=50)
    google_client_id: str = Field(default="")
    google_allowed_hd: str | None = Field(default=None)
    stripe: StripeSettings = Field(default_factory=StripeSettings)

    class Config:
        frozen = True


@functools.lru_cache
def get_settings() -> Settings:
    """Load settings from the environment with nested prefixes."""

    def _load(prefix: str) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                field = key.removeprefix(prefix).lower()
                data[field] = value
        return data

    stripe_cfg = _load("STRIPE_")
    stripe_settings = StripeSettings(
        secret_key=stripe_cfg.get("secret_key", ""),
        price_5=stripe_cfg.get("price_5", ""),
        price_10=stripe_cfg.get("price_10", ""),
        price_20=stripe_cfg.get("price_20", ""),
    )

    return Settings(
        mongo_uri=os.getenv("MONGO_URI", "mongodb://mongo:27017/tetris"),
        jwt_secret=os.getenv("JWT_SECRET", "change_me"),
        port=int(os.getenv("PORT", "8000")),
        rake_percent=int(os.getenv("RAKE_PERCENT", "10")),
        queue_timeout_ms=int(os.getenv("QUEUE_TIMEOUT_MS", "15000")),
        match_duration_ms=int(os.getenv("MATCH_DURATION_MS", "60000")),
        min_stake=int(os.getenv("MIN_STAKE", "50")),
        google_client_id=os.getenv("GOOGLE_CLIENT_ID", ""),
        google_allowed_hd=os.getenv("GOOGLE_ALLOWED_HD") or None,
        stripe=stripe_settings,
    )


settings = get_settings()
