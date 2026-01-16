import pytest

@pytest.mark.asyncio
async def test_access_students_without_token(client):
    """Endpoint /students/ powinien zwracać 401 bez nagłówka Authorization."""
    response = await client.get("/api/students/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"