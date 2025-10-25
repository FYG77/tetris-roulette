from __future__ import annotations

from datetime import datetime

from beanie import Document, Indexed
from pydantic import Field


class QueueEntry(Document):
    user_id: Indexed[str]
    stake_percent: Indexed[int]
    stake_amount: int
    enqueued_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "queue_entries"
