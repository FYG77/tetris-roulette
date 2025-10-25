from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.core.config import settings

ACCESS_TOKEN_TTL = timedelta(minutes=15)
REFRESH_TOKEN_TTL = timedelta(days=7)


class TokenService:
    def __init__(self, secret: str) -> None:
        self.secret = secret
        self.algorithm = "HS256"

    def create_token(self, subject: str, ttl: timedelta, extra: dict[str, Any] | None = None) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "iat": int(now.timestamp()),
            "exp": int((now + ttl).timestamp()),
        }
        if extra:
            payload.update(extra)
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_access_token(self, subject: str, extra: dict[str, Any] | None = None) -> str:
        return self.create_token(subject, ACCESS_TOKEN_TTL, extra)

    def create_refresh_token(self, subject: str) -> str:
        return self.create_token(subject, REFRESH_TOKEN_TTL)


token_service = TokenService(settings.jwt_secret)
