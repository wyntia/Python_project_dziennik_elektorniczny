import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime

from app.api.endpoints import router as api_router
from app.api.routes import status
from app.core.config import settings
from app.db.session import engine, Base
import app.models

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Logika wykonywana przy starcie i zamknięciu aplikacji.
    Tworzy tabele w bazie danych MySQL, jeśli nie istnieją.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root() -> dict:
    """Endpoint powitalny."""
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")
app.include_router(status.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)