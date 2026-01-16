import pytest

@pytest.mark.asyncio
async def test_add_remark(client, token_headers):
    s_resp = await client.post("/api/students/", json={
        "first_name": "Ola", "last_name": "Sól", "birth_date": "2012-05-05",
        "gender": "kobieta", "pesel": "12250512345"
    }, headers=token_headers)

    t_resp = await client.post("/api/teachers/", json={
        "first_name": "Jan",
        "last_name": "Belfer",
        "academic_degree": "mgr",
        "pesel": "70050511111"
    }, headers=token_headers)

    assert s_resp.status_code == 201, f"Błąd studenta: {s_resp.json()}"
    assert t_resp.status_code == 201, f"Błąd nauczyciela: {t_resp.json()}"

    student_id = s_resp.json()["id"]
    teacher_id = t_resp.json()["id"]

    remark_payload = {
        "description": "Bardzo aktywny udział w lekcji",
        "points": 10,
        "is_positive": True,
        "student_id": student_id,
        "teacher_id": teacher_id
    }
    response = await client.post("/api/remarks/", json=remark_payload, headers=token_headers)
    assert response.status_code == 201