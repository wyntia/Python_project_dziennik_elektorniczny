from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class User(Base):
    """
    Model SQLAlchemy reprezentujący użytkownika systemu posiadającego uprawnienia do logowania.

    Tabela przechowuje dane uwierzytelniające oraz status konta:
    - id: Unikalny identyfikator użytkownika (klucz główny).
    - username: Unikalna nazwa użytkownika używana podczas logowania.
    - hashed_password: Hasło użytkownika przechowywane w formie bezpiecznego haszu.
    - is_active: Flaga logiczna określająca, czy konto użytkownika jest obecnie aktywne.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)