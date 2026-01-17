import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.api.routes.teachers import assign_to_subject, add_teacher, edit_teacher, remove_teacher, list_teachers
from app.schemas import TeacherCreate, TeacherUpdate

@pytest.mark.asyncio
async def test_assign_teacher_to_subject_success():
    """Weryfikuje poprawne przypisanie nauczyciela do przedmiotu."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_teacher.assign_teacher_to_subject", new_callable=AsyncMock) as mock_assign:
        mock_assign.return_value = True
        result = await assign_to_subject(teacher_id=1, subject_id=5, db=mock_db)
        assert "pomyślnie przypisany" in result["message"]


@pytest.mark.asyncio
async def test_assign_teacher_to_subject_not_found():
    """Testuje błąd 404, gdy nauczyciel lub przedmiot nie istnieją."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_teacher.assign_teacher_to_subject", new_callable=AsyncMock) as mock_assign:
        mock_assign.return_value = False

        with pytest.raises(HTTPException) as exc:
            await assign_to_subject(teacher_id=1, subject_id=1, db=mock_db)

        assert exc.value.status_code == 404
        assert "Nie znaleziono nauczyciela lub przedmiotu" in exc.value.detail


@pytest.mark.asyncio
async def test_add_teacher_success_unit():
    """Testuje pomyślne dodanie nauczyciela."""
    mock_db = AsyncMock()
    payload = TeacherCreate(first_name="Anna", last_name="Nowak", academic_degree="mgr", pesel="85010111111")

    with patch("app.crud.crud_teacher.get_teacher_by_pesel", new_callable=AsyncMock) as mock_get, \
            patch("app.crud.crud_teacher.create_teacher", new_callable=AsyncMock) as mock_create:
        mock_get.return_value = None
        mock_create.return_value = MagicMock(id=1, **payload.model_dump())

        result = await add_teacher(teacher=payload, db=mock_db)
        assert result.last_name == "Nowak"


@pytest.mark.asyncio
async def test_edit_teacher_duplicate_pesel_error():
    """Testuje błąd 400, gdy przy edycji podamy PESEL innego nauczyciela."""
    mock_db = AsyncMock()
    data = TeacherUpdate(pesel="99999999999")

    with patch("app.crud.crud_teacher.get_teacher_by_pesel", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MagicMock(id=2, pesel="99999999999")

        with pytest.raises(HTTPException) as exc:
            await edit_teacher(teacher_id=1, data=data, db=mock_db)

        assert exc.value.status_code == 400
        assert "przypisany do innego nauczyciela" in exc.value.detail


@pytest.mark.asyncio
async def test_remove_teacher_not_found_unit():
    """Sprawdza błąd 404 przy usuwaniu nieistniejącego nauczyciela."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_teacher.delete_teacher", new_callable=AsyncMock) as mock_del:
        mock_del.return_value = False

        with pytest.raises(HTTPException) as exc:
            await remove_teacher(teacher_id=1, db=mock_db)
        assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_list_teachers_unit():
    """Testuje pobieranie listy wszystkich nauczycieli."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_teacher.get_teachers", new_callable=AsyncMock) as mock_list:
        t1 = MagicMock(); t1.last_name = "Kowalski"
        mock_list.return_value = [t1]
        result = await list_teachers(db=mock_db)
        assert len(result) == 1
        assert result[0].last_name == "Kowalski"