import pytest
from unittest.mock import AsyncMock, MagicMock
from app.crud.crud_student import create_student
from app.schemas.schemas import StudentCreate


@pytest.mark.asyncio
async def test_create_student_logic():
    """
    Test jednostkowy logiki tworzenia ucznia z wykorzystaniem Mockowania sesji.
    """
    # Mockowanie sesji bazy danych
    mock_db = AsyncMock(spec=AsyncSession)

    # Dane testowe
    student_data = StudentCreate(
        first_name="Jan",
        last_name="Kowalski",
        email="jan.kowalski@example.com"
    )

    # Wykonanie funkcji
    result = await create_student(mock_db, student_data)

    # Asercje
    assert result.first_name == "Jan"
    assert result.email == "jan.kowalski@example.com"
    mock_db.add.assert_called_once()
    assert mock_db.commit.called