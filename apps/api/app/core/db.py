from __future__ import annotations

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.match import Match
from app.models.queue import QueueEntry
from app.models.transaction import Transaction
from app.models.user import User


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[User, Transaction, Match, QueueEntry],
    )
