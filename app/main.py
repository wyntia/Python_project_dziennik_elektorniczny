import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime

from app.api.endpoints import router as api_router
from app.core.config import settings
from app.db.session import engine, Base
from app.models import Student, Subject, Grade

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

@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Asynchroniczny WebSocket zwracający status serwera co 5 sekund.
    Zgodnie z wymogiem: format JSON (status, data i godzina).
    """
    await websocket.accept()
    try:
        while True:
            data = {
                "status": "online",
                "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "project": settings.PROJECT_NAME
            }
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)