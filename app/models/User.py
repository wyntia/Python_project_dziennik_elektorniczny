from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class User(Base):
    """
    Model reprezentujący użytkownika systemu zdolnego do logowania.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)