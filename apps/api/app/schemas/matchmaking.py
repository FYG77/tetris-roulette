from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class QueueJoinRequest(BaseModel):
    stake_percent: int = Field(..., description="Stake percentage")


class QueueLeaveRequest(BaseModel):
    pass


class MatchSummary(BaseModel):
    id: str
    stake_percent: int
    seed: str
    status: str
    started_at: datetime | None
    ended_at: datetime | None
    pot: int
    rake_percent: int
    participants: list[str]
    scores: dict[str, int]
    winner_user_id: str | None
