from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.auth.deps import get_current_user
from app.core.config import settings
from app.models.queue import QueueEntry
from app.schemas.matchmaking import QueueJoinRequest

router = APIRouter(prefix="/queue", tags=["queue"])


@router.post("/join")
async def join_queue(payload: QueueJoinRequest, current_user=Depends(get_current_user)) -> dict[str, str]:  # type: ignore[annotation-unchecked]
    stake_amount = (current_user.coins * payload.stake_percent) // 100
    if payload.stake_percent not in {5, 10, 20}:
        raise HTTPException(status_code=400, detail="Invalid stake percent")
    if stake_amount < settings.min_stake:
        raise HTTPException(status_code=400, detail="Insufficient balance for minimum stake")

    existing = await QueueEntry.find_one(QueueEntry.user_id == str(current_user.id))
    if existing:
        return {"status": "already_enqueued"}

    entry = QueueEntry(
        user_id=str(current_user.id),
        stake_percent=payload.stake_percent,
        stake_amount=stake_amount,
        enqueued_at=datetime.utcnow(),
    )
    await entry.insert()
    return {"status": "enqueued"}


@router.post("/leave")
async def leave_queue(current_user=Depends(get_current_user)) -> dict[str, str]:  # type: ignore[annotation-unchecked]
    entry = await QueueEntry.find_one(QueueEntry.user_id == str(current_user.id))
    if entry:
        await entry.delete()
    return {"status": "removed"}
