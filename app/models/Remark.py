from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Remark(Base):
    """
    Model SQLAlchemy reprezentujący uwagę wystawioną uczniowi przez nauczyciela.
    Przechowuje punkty, opis oraz informację, czy uwaga jest pozytywna czy negatywna.
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