from __future__ import annotations

import httpx
from fastapi import HTTPException, status
from jose import jwt
from pydantic import BaseModel

from app.core.config import settings
from app.models.user import User

GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"
ALGORITHMS = ["RS256"]


class GoogleTokenPayload(BaseModel):
    iss: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    name: str | None = None
    picture: str | None = None


async def verify_google_token(id_token: str) -> GoogleTokenPayload:
    """Fetch Google's certs and verify the provided id_token."""
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_CERTS_URL, timeout=5)
        response.raise_for_status()
        certs = response.json()

    try:
        payload = jwt.decode(
            id_token,
            certs,
            algorithms=ALGORITHMS,
            audience=settings.google_client_id,
        )
        data = GoogleTokenPayload(**payload)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token") from exc

    if settings.google_allowed_hd:
        hosted_domain = payload.get("hd")
        if hosted_domain != settings.google_allowed_hd:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Domain not allowed")

    if not data.email_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not verified")

    return data


async def upsert_user_from_google(payload: GoogleTokenPayload) -> User:
    existing = await User.find_one(User.google_sub == payload.sub)
    if existing:
        existing.email = payload.email
        existing.avatar_url = payload.picture
        await existing.save()
        return existing

    handle_base = payload.email.split("@")[0]
    handle_candidate = handle_base
    idx = 1
    while await User.find_one(User.handle == handle_candidate):
        idx += 1
        handle_candidate = f"{handle_base}{idx}"

    user = User(
        google_sub=payload.sub,
        email=payload.email,
        handle=handle_candidate,
        avatar_url=payload.picture,
    )
    await user.insert()
    return user
