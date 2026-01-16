from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.User import User
from app.core import security
from app.schemas.user import Token
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    Loguje użytkownika i zwraca token JWT.
    Login: admin
    Hasło: admin123
    """
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Niepoprawny login lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(subject=user.username)
    return Token(access_token=access_token, token_type="bearer")

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Wylogowanie w systemie JWT polega na usunięciu tokena po stronie klienta.
    Ten endpoint potwierdza zakończenie sesji dla zalogowanego użytkownika.
    """
    return {"message": f"Użytkownik {current_user.username} został wylogowany. Usuń token z pamięci aplikacji."}