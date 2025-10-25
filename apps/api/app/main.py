from __future__ import annotations

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.db import init_db
from app.routes import admin, auth, matches, queue, wallet

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI(title="Tetris Roulette API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()


app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(queue.router)
app.include_router(matches.router)
app.include_router(admin.router)

socket_app = socketio.ASGIApp(sio, other_asgi_app=app)


@sio.event(namespace="/game")
async def connect(sid, environ):  # type: ignore[no-untyped-def]
    await sio.emit("connected", {"sid": sid}, room=sid, namespace="/game")


@sio.on("queue.join", namespace="/game")
async def handle_queue_join(sid, data):  # type: ignore[no-untyped-def]
    await sio.emit("queue.ack", data, to=sid, namespace="/game")


@sio.event(namespace="/game")
async def disconnect(sid):  # type: ignore[no-untyped-def]
    await sio.emit("disconnect", {"sid": sid}, namespace="/game")


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("app.main:socket_app", host="0.0.0.0", port=settings.port, reload=True)
