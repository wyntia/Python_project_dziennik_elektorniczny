import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.api.routes.auth import login_for_access_token, logout


@pytest.mark.asyncio
async def test_login_invalid_user_raises_exception():
    """Testuje, czy próba logowania nieistniejącego użytkownika wyrzuca błąd 401."""
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    mock_form = MagicMock()
    mock_form.username = "nonexistent"
    mock_form.password = "any_password"

    with pytest.raises(HTTPException) as exc:
        await login_for_access_token(db=mock_db, form_data=mock_form)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Niepoprawny login lub hasło"


@pytest.mark.asyncio
async def test_logout_unit():
    """Weryfikuje odpowiedź serwera po wylogowaniu."""
    mock_user = MagicMock(username="admin")
    result = await logout(current_user=mock_user)

    assert "został wylogowany" in result["message"]
    assert "admin" in result["message"]