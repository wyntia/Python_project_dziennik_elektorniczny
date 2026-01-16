from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

teacher_subject = Table(
    "teacher_subject",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True)
)

class Teacher(Base):
    """
    Model SQLAlchemy reprezentujący nauczyciela w systemie dziennika.
    Przechowuje dane osobowe oraz relacje do nauczanych przedmiotów.
    """
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    academic_degree = Column(String(50), nullable=False)  # np. mgr, dr, prof.
    pesel = Column(String(11), unique=True, index=True, nullable=False)

    subjects = relationship(
        "Subject",
        secondary=teacher_subject,
        back_populates="teachers",
        lazy="selectin"
    )

    remarks = relationship(
        "Remark",
        back_populates="teacher",
        lazy="selectin"
    )