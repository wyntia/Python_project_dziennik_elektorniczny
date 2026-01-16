import pytest

@pytest.mark.asyncio
async def test_create_subject(client, token_headers):
    response = await client.post("/api/subjects/", json={"name": "Matematyka"}, headers=token_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Matematyka"

@pytest.mark.asyncio
async def test_create_duplicate_subject(client, token_headers):
    await client.post("/api/subjects/", json={"name": "Fizyka"}, headers=token_headers)
    response = await client.post("/api/subjects/", json={"name": "Fizyka"}, headers=token_headers)
    assert response.status_code == 400
    assert "już istnieje" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_subjects_list(client, token_headers):
    await client.post("/api/subjects/", json={"name": "Chemia"}, headers=token_headers)
    response = await client.get("/api/subjects/", headers=token_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1