from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.auth.deps import get_current_user
from app.models.match import Match
from app.schemas.matchmaking import MatchSummary

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/{match_id}", response_model=MatchSummary)
async def get_match(match_id: str, current_user=Depends(get_current_user)) -> MatchSummary:  # type: ignore[annotation-unchecked]
    match = await Match.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return MatchSummary(
        id=str(match.id),
        stake_percent=match.stake_percent,
        seed=match.seed,
        status=match.status,
        started_at=match.started_at,
        ended_at=match.ended_at,
        pot=match.pot,
        rake_percent=match.rake_percent,
        participants=match.participants,
        scores=match.scores,
        winner_user_id=match.winner_user_id,
    )
