from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Grade(Base):
    """
    Model reprezentujący ocenę wystawioną uczniowi.
    Zawiera wartość (np. '5+'), wagę oraz opis.
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