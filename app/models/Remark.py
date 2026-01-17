from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Remark(Base):
    """
    Model SQLAlchemy reprezentujący formalną uwagę (pochwałę lub naganę) wystawioną uczniowi.

    Rejestruje szczegóły zachowania oraz powiązania między uczniem a nauczycielem:
    - id: Numer identyfikacyjny uwagi.
    - points: Liczba punktów (dodatnich lub ujemnych) wpływających na ocenę z zachowania.
    - description: Treść uwagi opisująca konkretne zdarzenie lub postawę.
    - is_positive: Flaga określająca, czy uwaga ma charakter pozytywny.
    - student_id: Klucz obcy łączący uwagę z konkretnym uczniem.
    - teacher_id: Klucz obcy wskazujący nauczyciela, który wystawił uwagę.
    - created_at: Data i czas utworzenia wpisu, generowane automatycznie przez serwer bazy danych.

    Powiązania:
    - student: Obiekt ucznia, którego dotyczy uwaga.
    - teacher: Obiekt nauczyciela będącego autorem wpisu.
    """
    __tablename__ = "remarks"

    id = Column(Integer, primary_key=True, index=True)
    points = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    is_positive = Column(Boolean, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="remarks")
    teacher = relationship("Teacher", back_populates="remarks")