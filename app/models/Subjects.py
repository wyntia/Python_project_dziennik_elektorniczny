from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Subject(Base):
    """
    Model reprezentujący przedmiot szkolny z opcjonalnym opisem.
    """
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    grades = relationship("Grade", back_populates="subject", lazy="selectin")