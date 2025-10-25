from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class GoogleAuthRequest(BaseModel):
    id_token: str = Field(min_length=10)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class UserProfile(BaseModel):
    id: str
    email: EmailStr
    handle: str
    avatar_url: str | None = None
    coins: int
    created_at: datetime
