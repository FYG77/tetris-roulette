# Tetris Roulette

This repository contains a monorepo-style layout for the **Tetris Game Roulette** MVP. It includes a FastAPI backend, a Vite/React frontend, and infrastructure configuration for local Docker-based development.

## Structure

```
apps/
  api/           # FastAPI backend (Socket.IO, Mongo/Beanie)
  web/           # React + Vite frontend
  infra/         # Docker Compose, nginx
```

## Backend quick start

```bash
cd apps/api
pip install -e .[dev]
uvicorn app.main:socket_app --reload
```

## Running tests

```bash
cd apps/api
pytest
```

Populate the `.env` file from `.env.example` before running the stack.
