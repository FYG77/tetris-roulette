from __future__ import annotations

import stripe
from fastapi import APIRouter, Depends, HTTPException

from app.auth.deps import get_current_user
from app.core.config import settings
from app.models.transaction import Transaction
from app.schemas.wallet import BalanceResponse, CheckoutRequest, CheckoutResponse

router = APIRouter(prefix="/wallet", tags=["wallet"])

stripe.api_key = settings.stripe.secret_key


@router.get("/balance", response_model=BalanceResponse)
async def get_balance(current_user=Depends(get_current_user)) -> BalanceResponse:  # type: ignore[annotation-unchecked]
    return BalanceResponse(coins=current_user.coins)


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout_session(
    payload: CheckoutRequest,
    current_user=Depends(get_current_user),  # type: ignore[annotation-unchecked]
) -> CheckoutResponse:
    price_lookup = {
        "pack5": settings.stripe.price_5,
        "pack10": settings.stripe.price_10,
        "pack20": settings.stripe.price_20,
    }
    price_id = price_lookup.get(payload.pack_id)
    if not price_id:
        raise HTTPException(status_code=400, detail="Unknown pack")

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url="https://localhost/success",
        cancel_url="https://localhost/cancel",
        client_reference_id=str(current_user.id),
        metadata={"user_id": str(current_user.id)},
    )
    return CheckoutResponse(checkout_url=session.url)


@router.post("/webhook")
async def stripe_webhook(payload: dict[str, object]) -> dict[str, str]:
    event_type = payload.get("type")
    data = payload.get("data", {})
    if event_type == "checkout.session.completed" and isinstance(data, dict):
        session_data = data.get("object", {})
        if isinstance(session_data, dict):
            user_id = session_data.get("client_reference_id")
            amount_total = session_data.get("amount_total", 0)
            if user_id:
                txn = Transaction(
                    user_id=str(user_id),
                    ttype="PURCHASE",
                    amount=int(amount_total),
                    meta={"session": session_data.get("id")},
                )
                await txn.insert()
    return {"status": "ok"}
