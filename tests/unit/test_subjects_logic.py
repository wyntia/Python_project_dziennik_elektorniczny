import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.api.routes.subjects import create_new_subject, read_subjects, update_subject, read_subject, delete_subject
from app.schemas import SubjectCreate, SubjectUpdate


@pytest.mark.asyncio
async def test_create_subject_duplicate_name():
    """Testuje blokadę duplikatów nazw przedmiotów."""
    mock_db = AsyncMock()
    mock_data = SubjectCreate(name="Matematyka")

    with patch("app.crud.crud_subject.get_subject_by_name", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MagicMock(id=1)

        with pytest.raises(HTTPException) as exc:
            await create_new_subject(subject=mock_data, db=mock_db)

        assert exc.value.status_code == 400
        assert "już istnieje" in exc.value.detail


@pytest.mark.asyncio
async def test_read_subjects_unit():
    """Testuje pobieranie listy wszystkich przedmiotów."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_subject.get_subjects", new_callable=AsyncMock) as mock_list:
        mock_math = MagicMock()
        mock_math.name = "Matematyka"
        mock_phys = MagicMock()
        mock_phys.name = "Fizyka"

        mock_list.return_value = [mock_math, mock_phys]

        result = await read_subjects(db=mock_db)

        assert len(result) == 2
        assert result[0].name == "Matematyka"
        assert result[1].name == "Fizyka"


@pytest.mark.asyncio
async def test_read_subject_success_unit():
    """Testuje pobieranie pojedynczego przedmiotu po ID."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_subject.get_subject", new_callable=AsyncMock) as mock_get:
        mock_subj = MagicMock(); mock_subj.name = "Historia"
        mock_get.return_value = mock_subj
        result = await read_subject(subject_id=1, db=mock_db)
        assert result.name == "Historia"

@pytest.mark.asyncio
async def test_delete_subject_success_unit():
    """Weryfikuje pomyślne usunięcie przedmiotu."""
    mock_db = AsyncMock()
    with patch("app.crud.crud_subject.delete_subject", new_callable=AsyncMock) as mock_del:
        mock_del.return_value = True
        result = await delete_subject(subject_id=1, db=mock_db)
        assert "pomyślnie usunięty" in result["message"]


@pytest.mark.asyncio
async def test_update_subject_duplicate_name_error():
    """Sprawdza błąd 400 przy zmianie nazwy na już istniejącą."""
    mock_db = AsyncMock()
    data = SubjectUpdate(name="Historia")

    with patch("app.crud.crud_subject.get_subject_by_name", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MagicMock(id=5, name="Historia")

        with pytest.raises(HTTPException) as exc:
            await update_subject(subject_id=1, subject_data=data, db=mock_db)

        assert exc.value.status_code == 400
        assert "już istnieje" in exc.value.detail