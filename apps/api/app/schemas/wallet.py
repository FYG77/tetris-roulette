from __future__ import annotations

from pydantic import BaseModel, Field


class BalanceResponse(BaseModel):
    coins: int


class CheckoutRequest(BaseModel):
    pack_id: str = Field(min_length=3)


class CheckoutResponse(BaseModel):
    checkout_url: str
