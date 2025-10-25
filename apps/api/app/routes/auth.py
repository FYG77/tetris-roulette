from __future__ import annotations

from fastapi import APIRouter, Depends, Response

from app.auth.deps import get_current_user
from app.schemas.auth import GoogleAuthRequest, TokenPair, UserProfile
from app.services import auth_service
from app.services.token_service import token_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google", response_model=UserProfile)
async def google_auth(payload: GoogleAuthRequest, response: Response) -> UserProfile:
    google_payload = await auth_service.verify_google_token(payload.id_token)
    user = await auth_service.upsert_user_from_google(google_payload)
    access_token = token_service.create_access_token(str(user.id))
    refresh_token = token_service.create_refresh_token(str(user.id))
    response.set_cookie("access_token", access_token, httponly=True, secure=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True)
    return UserProfile(
        id=str(user.id),
        email=user.email,
        handle=user.handle,
        avatar_url=user.avatar_url,
        coins=user.coins,
        created_at=user.created_at,
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(current_user=Depends(get_current_user)) -> TokenPair:  # type: ignore[annotation-unchecked]
    access_token = token_service.create_access_token(str(current_user.id))
    refresh_token = token_service.create_refresh_token(str(current_user.id))
    return TokenPair(access_token=access_token, refresh_token=refresh_token, expires_in=900)


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"status": "logged_out"}
