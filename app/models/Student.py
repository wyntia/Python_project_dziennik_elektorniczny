from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

class Student(Base):
    """
    Model SQLAlchemy reprezentujący ucznia w systemie dziennika elektronicznego.

    Przechowuje kluczowe dane osobowe oraz zarządza powiązanymi z uczniem rekordami edukacyjnymi:
    - id: Unikalny identyfikator ucznia.
    - first_name: Imię ucznia.
    - last_name: Nazwisko ucznia.
    - birth_date: Data urodzenia ucznia.
    - gender: Płeć ucznia.
    - pesel: Unikalny, 11-cyfrowy numer identyfikacyjny PESEL.

    Relacje z automatycznym usuwaniem kaskadowym:
    - grades: Wszystkie oceny przypisane do ucznia; usunięcie ucznia powoduje usunięcie jego ocen.
    - remarks: Wszystkie uwagi wystawione uczniowi; usunięcie ucznia powoduje usunięcie jego uwag.
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

    remarks = relationship(
        "Remark",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="selectin"
    )