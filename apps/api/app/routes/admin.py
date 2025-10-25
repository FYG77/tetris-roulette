from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.auth.deps import get_admin_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/ban")
async def ban_user(payload: dict[str, object], admin=Depends(get_admin_user)) -> dict[str, str]:  # type: ignore[annotation-unchecked]
    user_id = payload.get("userId")
    is_banned = bool(payload.get("isBanned", True))
    if not user_id:
        raise HTTPException(status_code=400, detail="userId required")
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_banned = is_banned
    await user.save()
    return {"status": "updated"}
