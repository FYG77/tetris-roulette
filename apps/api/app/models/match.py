from __future__ import annotations

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class Match(Document):
    stake_percent: int
    seed: str
    status: Indexed[str]
    started_at: datetime | None = None
    ended_at: datetime | None = None
    pot: int = 0
    rake_percent: int = 10
    is_house_match: bool = False
    participants: list[str] = Field(default_factory=list)
    scores: dict[str, int] = Field(default_factory=dict)
    winner_user_id: Optional[str] = None
    audit_urls: dict[str, str] = Field(default_factory=dict)

    class Settings:
        name = "matches"
