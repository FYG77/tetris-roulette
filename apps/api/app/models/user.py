from __future__ import annotations

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class User(Document):
    google_sub: Indexed(str, unique=True)
    email: Indexed(str, unique=True)
    handle: Indexed(str, unique=True)
    avatar_url: Optional[str] = None
    region: Optional[str] = None
    coins: int = 1000
    is_banned: bool = False
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
