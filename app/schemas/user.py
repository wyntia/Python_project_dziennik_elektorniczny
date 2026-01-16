from pydantic import BaseModel, ConfigDict
from typing import Optional


class Token(BaseModel):
    """
    Schemat odpowiedzi zawierający token dostępu JWT.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schemat danych zakodowanych wewnątrz tokena JWT.
    """
    username: Optional[str] = None


class UserCreate(BaseModel):
    """
    Schemat danych wymaganych do utworzenia nowego użytkownika.
    """
    username: str
    password: str


class User(BaseModel):
    """
    Pełny schemat użytkownika zwracany przez system.
    """
    id: int
    username: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)