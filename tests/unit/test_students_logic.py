import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.api.routes.students import add_student, get_student, edit_student, list_students, remove_student
from app.schemas import StudentCreate, StudentUpdate


@pytest.mark.asyncio
async def test_add_student_duplicate_pesel_unit():
    """Testuje czy API rzuca błąd 400 przy powtórzonym PESEL."""
    mock_db = AsyncMock()
    mock_student_data = StudentCreate(
        first_name="Jan", last_name="K", birth_date="2000-01-01",
        gender="mężczyzna", pesel="12345678901"
    )

    with patch("app.crud.crud_student.get_student_by_pesel", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MagicMock(id=1)

        with pytest.raises(HTTPException) as exc:
            await add_student(student=mock_student_data, db=mock_db)

        assert exc.value.status_code == 400
        assert "już figuruje w bazie" in exc.value.detail


@pytest.mark.asyncio
async def test_edit_student_duplicate_pesel_other_user():
    """Testuje błąd 400, gdy zmieniamy PESEL na taki, który ma już inny uczeń."""
    mock_db = AsyncMock()
    update_data = StudentUpdate(pesel="99999999999")

    with patch("app.crud.crud_student.get_student_by_pesel", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MagicMock(id=2, pesel="99999999999")

        with pytest.raises(HTTPException) as exc:
            await edit_student(student_id=1, student_data=update_data, db=mock_db)
        assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_get_nonexistent_student_unit():
    """Sprawdza reakcję na żądanie nieistniejącego ID."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_student.get_student", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = None

        with pytest.raises(HTTPException) as exc:
            await get_student(student_id=999, db=mock_db)

        assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_add_student_success_unit():
    """Testuje poprawne dodanie ucznia przy użyciu mocków."""
    mock_db = AsyncMock()
    mock_student_data = StudentCreate(
        first_name="Jan", last_name="Kowalski", birth_date="2010-05-15",
        gender="mężczyzna", pesel="12345678901"
    )

    with patch("app.crud.crud_student.get_student_by_pesel", new_callable=AsyncMock) as mock_get, \
            patch("app.crud.crud_student.create_student", new_callable=AsyncMock) as mock_create:
        mock_get.return_value = None  # PESEL nie istnieje
        mock_create.return_value = MagicMock(id=1, **mock_student_data.model_dump())

        result = await add_student(student=mock_student_data, db=mock_db)

        assert result.first_name == "Jan"
        mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_edit_student_success_unit():
    """Weryfikuje poprawną edycję danych ucznia."""
    mock_db = AsyncMock()
    update_data = StudentUpdate(first_name="Adam")

    with patch("app.crud.crud_student.update_student", new_callable=AsyncMock) as mock_update:
        mock_update.return_value = MagicMock(id=1, first_name="Adam", last_name="Kowalski")

        result = await edit_student(student_id=1, student_data=update_data, db=mock_db)

        assert result.first_name == "Adam"
        mock_update.assert_called_once_with(mock_db, 1, update_data)

@pytest.mark.asyncio
async def test_list_students_unit():
    """Weryfikuje pobieranie listy uczniów."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_student.get_students", new_callable=AsyncMock) as mock_get:
        s1 = MagicMock(); s1.first_name = "Jan"
        s2 = MagicMock(); s2.first_name = "Anna"
        mock_get.return_value = [s1, s2]

        result = await list_students(db=mock_db)
        assert len(result) == 2
        assert result[0].first_name == "Jan"

@pytest.mark.asyncio
async def test_remove_student_success_unit():
    """Weryfikuje pomyślne usunięcie ucznia."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_student.delete_student", new_callable=AsyncMock) as mock_del:
        mock_del.return_value = True
        result = await remove_student(student_id=1, db=mock_db)
        assert "został usunięty" in result["message"]

@pytest.mark.asyncio
async def test_remove_student_not_found():
    """Sprawdza błąd 404 przy usuwaniu nieistniejącego ucznia."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_student.delete_student", new_callable=AsyncMock) as mock_del:
        mock_del.return_value = False
        with pytest.raises(HTTPException) as exc:
            await remove_student(student_id=999, db=mock_db)
        assert exc.value.status_code == 404