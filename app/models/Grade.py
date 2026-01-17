from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Grade(Base):
    """
    Model SQLAlchemy reprezentujący ocenę cząstkową wystawioną uczniowi z danego przedmiotu.

    Zawiera informacje o wartości edukacyjnej oraz kontekście wystawienia stopnia:
    - id: Unikalny identyfikator oceny.
    - value: Wartość tekstowa oceny (np. '1', '5+', '4-').
    - weight: Waga oceny używana do obliczania średniej ważonej (domyślnie 1.0).
    - description: Opcjonalny opis (np. 'Sprawdzian z dynamiki', 'Odpowiedź ustna').
    - student_id: Klucz obcy powiązany z uczniem otrzymującym ocenę.
    - subject_id: Klucz obcy wskazujący przedmiot, z którego wystawiono ocenę.
    - created_at: Znacznik czasu rejestrujący moment wystawienia oceny.

    Powiązania:
    - student: Referencja do obiektu ucznia.
    - subject: Referencja do obiektu przedmiotu szkolnego.
    """
    __tablename__ = "grades"

    id: int = Column(Integer, primary_key=True, index=True)
    value: str = Column(String(3), nullable=False)
    weight: float = Column(Float, default=1.0, nullable=False)
    description: str = Column(Text, nullable=True)
    student_id: int = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id: int = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")