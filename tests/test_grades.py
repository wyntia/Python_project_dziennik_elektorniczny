import pytest


@pytest.mark.asyncio
async def test_add_grade_to_student(client, token_headers):
    s_resp = await client.post("/api/students/",
                               json={"first_name": "Marek", "last_name": "Zegar", "birth_date": "2010-01-01",
                                     "gender": "mężczyzna", "pesel": "10210199999"}, headers=token_headers)
    sub_resp = await client.post("/api/subjects/", json={"name": "Informatyka"}, headers=token_headers)

    student_id = s_resp.json()["id"]
    subject_id = sub_resp.json()["id"]

    grade_payload = {
        "value": "5",
        "weight": 2.0,
        "description": "Sprawdzian",
        "subject_id": subject_id,
        "student_id": student_id
    }
    response = await client.post("/api/grades/", json=grade_payload, headers=token_headers)
    assert response.status_code == 201
    assert response.json()["value"] == "5"


@pytest.mark.asyncio
async def test_get_student_grades(client, token_headers):
    response = await client.get("/api/grades/student/1", headers=token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)