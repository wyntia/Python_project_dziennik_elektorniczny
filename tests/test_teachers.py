import pytest


@pytest.mark.asyncio
async def test_create_teacher(client, token_headers):
    payload = {
        "first_name": "Adam",
        "last_name": "Nowak",
        "academic_degree": "mgr",
        "pesel": "80010112345"
    }
    response = await client.post("/api/teachers/", json=payload, headers=token_headers)
    assert response.status_code == 201
    assert response.json()["last_name"] == "Nowak"


@pytest.mark.asyncio
async def test_assign_teacher_to_subject(client, token_headers):
    teacher_data = {
        "first_name": "Ewa",
        "last_name": "Bąk",
        "academic_degree": "dr",
        "pesel": "90010155555"
    }
    t_resp = await client.post("/api/teachers/", json=teacher_data, headers=token_headers)
    s_resp = await client.post("/api/subjects/", json={"name": "Biologia"}, headers=token_headers)

    assert t_resp.status_code == 201
    assert s_resp.status_code == 201

    t_id = t_resp.json()["id"]
    s_id = s_resp.json()["id"]

    response = await client.post(f"/api/teachers/{t_id}/assign/{s_id}", headers=token_headers)
    assert response.status_code == 200