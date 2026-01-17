import asyncio
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws/server-status")
async def websocket_server_status(websocket: WebSocket) -> None:
    """
    Asynchroniczny WebSocket zwracający aktualne informacje o serwerze w formacie JSON.
    Wymaganie: Status, data i godzina.
    """
    await websocket.accept()
    try:
        while True:
            status_info = {
                "status": "running",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "server_name": "FastAPI Gradebook Server"
            }
            await websocket.send_json(status_info)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Połączenie WebSocket zostało zamknięte.")