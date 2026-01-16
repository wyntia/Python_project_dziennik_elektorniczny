import pytest


@pytest.fixture
async def token_headers(client, db_session):
    """Pomocnicza fixture tworząca zalogowanego admina i zwracająca nagłówki."""
    from app.core.security import get_password_hash, create_access_token
    from app.models.User import User

    user = User(username="admin", hashed_password=get_password_hash("pass"), is_active=True)
    db_session.add(user)
    await db_session.commit()

    token = create_access_token(subject="admin")
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_student(client, token_headers):
    payload = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "birth_date": "2010-05-15",
        "gender": "mężczyzna",
        "pesel": "12345678901"
    }
    response = await client.post("/api/students/", json=payload, headers=token_headers)
    assert response.status_code == 201
    assert response.json()["first_name"] == "Jan"
    assert "id" in response.json()


@pytest.mark.asyncio
async def test_duplicate_pesel_error(client, token_headers):
    payload = {
        "first_name": "Anna", "last_name": "Nowak", "birth_date": "2011-01-01",
        "gender": "kobieta", "pesel": "11111111111"
    }
    await client.post("/api/students/", json=payload, headers=token_headers)

    response = await client.post("/api/students/", json=payload, headers=token_headers)
    assert response.status_code == 400
    assert "już figuruje w bazie" in response.json()["detail"]