from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.Teacher import teacher_subject

class Subject(Base):
    """
    Model SQLAlchemy reprezentujący przedmiot szkolny (np. Matematyka, Fizyka).

    Klasa definiuje strukturę danych przedmiotu oraz jego powiązania z ocenami i kadrą nauczycielską:
    - id: Unikalny identyfikator przedmiotu.
    - name: Unikalna nazwa przedmiotu.
    - description: Opcjonalny, rozszerzony opis programu lub charakterystyki przedmiotu.

    Relacje:
    - grades: Lista ocen wystawionych w ramach tego przedmiotu (relacja jeden-do-wielu).
    - teachers: Zbiór nauczycieli prowadzących dany przedmiot (relacja wiele-do-wielu realizowana przez tabelę teacher_subject).
    """
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    grades = relationship("Grade", back_populates="subject", lazy="selectin")

    teachers = relationship(
        "Teacher",
        secondary=teacher_subject,
        back_populates="subjects",
        lazy="selectin"
    )