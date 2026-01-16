import pytest
from app.core.security import get_password_hash
from app.models.User import User


@pytest.mark.asyncio
async def test_login_success(client, db_session):
    hashed_pw = get_password_hash("testpass")
    user = User(username="testuser", hashed_password=hashed_pw, is_active=True)
    db_session.add(user)
    await db_session.commit()

    response = await client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpass"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client, db_session):
    response = await client.post("/api/auth/login", data={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 401