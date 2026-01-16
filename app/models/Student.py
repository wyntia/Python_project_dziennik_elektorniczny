from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

class Student(Base):
    """
    Model SQLAlchemy reprezentujący ucznia.
    Przechowuje dane osobowe, w tym unikalny PESEL.
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    pesel = Column(String(11), unique=True, index=True, nullable=False)

    grades = relationship(
        "Grade",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="selectin"
    )