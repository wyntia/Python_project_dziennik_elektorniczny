import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.api.routes.remarks import edit_remark, read_student_remarks, add_remark, remove_remark
from app.schemas import RemarkUpdate, RemarkCreate


@pytest.mark.asyncio
async def test_add_remark_success_unit():
    """Weryfikuje poprawne wystawienie uwagi."""
    mock_db = AsyncMock()
    remark_data = RemarkCreate(points=-5, description="Spóźnienie", is_positive=False, student_id=1, teacher_id=2)

    with patch("app.crud.crud_remark.create_remark", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = MagicMock(id=1, points=-5)
        result = await add_remark(remark=remark_data, db=mock_db)
        assert result.points == -5


@pytest.mark.asyncio
async def test_remove_remark_success_unit():
    """Testuje pomyślne usunięcie uwagi."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_remark.delete_remark", new_callable=AsyncMock) as mock_del:
        mock_del.return_value = True
        result = await remove_remark(remark_id=1, db=mock_db)
        assert "pomyślnie usunięta" in result["message"]


@pytest.mark.asyncio
async def test_edit_nonexistent_remark():
    """Sprawdza błąd 404 przy edycji braku uwagi."""
    mock_db = AsyncMock()
    mock_data = RemarkUpdate(points=-10)

    with patch("app.crud.crud_remark.update_remark", new_callable=AsyncMock) as mock_upd:
        mock_upd.return_value = None

        with pytest.raises(HTTPException) as exc:
            await edit_remark(remark_id=1, remark_data=mock_data, db=mock_db)

        assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_read_student_remarks_unit():
    """Testuje pobieranie uwag przypisanych do ucznia."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_remark.get_student_remarks", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [MagicMock(points=10, description="Pochwała")]

        result = await read_student_remarks(student_id=1, db=mock_db)
        assert len(result) == 1
        assert result[0].points == 10