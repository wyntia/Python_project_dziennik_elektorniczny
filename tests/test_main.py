import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint() -> None:
    """
    Testuje czy główny endpoint API zwraca poprawny status i wiadomość.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert "Witamy" in response.json()["message"]


@pytest.mark.asyncio
async def test_websocket_status() -> None:
    """
    Testuje połączenie WebSocket (uproszczony test dostępności).
    W środowisku testowym FastAPI używamy test_client do symulacji WebSocket.
    """
    from fastapi.testclient import TestClient
    client = TestClient(app)
    with client.websocket_connect("/ws/status") as websocket:
        data = websocket.receive_json()
        assert data["status"] == "online"
        assert "server_time" in data