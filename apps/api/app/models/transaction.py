from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from beanie import Document, Indexed
from pydantic import Field


class Transaction(Document):
    user_id: Indexed[str]
    ttype: str
    amount: int
    meta: Optional[dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "transactions"
