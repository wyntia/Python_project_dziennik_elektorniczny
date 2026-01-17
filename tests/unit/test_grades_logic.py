import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.api.routes.grades import delete_grade, get_student_grades, edit_grade, add_grade
from app.schemas import GradeUpdate, GradeCreate


@pytest.mark.asyncio
async def test_add_grade_success_unit():
    """Testuje pomyślne wystawienie nowej oceny."""
    mock_db = AsyncMock()
    grade_data = GradeCreate(value="5", weight=2.0, student_id=1, subject_id=1)

    with patch("app.crud.crud_grade.create_grade", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = MagicMock(id=10, value="5")
        result = await add_grade(grade=grade_data, db=mock_db)
        assert result.value == "5"
        mock_create.assert_called_once()


@pytest.mark.asyncio
async def test_delete_grade_success_unit():
    """Weryfikuje pomyślne usunięcie oceny."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_grade.delete_grade", new_callable=AsyncMock) as mock_del:
        mock_del.return_value = True
        result = await delete_grade(grade_id=1, db=mock_db)
        assert "została pomyślnie usunięty" in result["message"]


@pytest.mark.asyncio
async def test_delete_grade_not_found():
    """Weryfikuje błąd 404 przy próbie usunięcia nieistniejącej oceny."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_grade.delete_grade", new_callable=AsyncMock) as mock_del:
        mock_del.return_value = False

        with pytest.raises(HTTPException) as exc:
            await delete_grade(grade_id=99, db=mock_db)

        assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_get_student_grades_unit():
    """Weryfikuje pobieranie listy ocen dla konkretnego ucznia."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_grade.get_student_grades", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [MagicMock(value="5", weight=2.0), MagicMock(value="4")]

        result = await get_student_grades(student_id=1, db=mock_db)
        assert len(result) == 2
        assert result[0].value == "5"


@pytest.mark.asyncio
async def test_edit_grade_success_unit():
    """Weryfikuje poprawną edycję oceny."""
    mock_db = AsyncMock()
    update_data = GradeUpdate(value="5", weight=3.0)

    with patch("app.crud.crud_grade.update_grade", new_callable=AsyncMock) as mock_update:
        mock_result = MagicMock()
        mock_result.value = "5"
        mock_update.return_value = mock_result

        result = await edit_grade(grade_id=1, grade_data=update_data, db=mock_db)
        assert result.value == "5"
        mock_update.assert_called_once()