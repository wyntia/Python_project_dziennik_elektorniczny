from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional
from datetime import datetime

GradeValue = Literal["1", "2-", "2+", "3-", "3+", "4", "4-", "4+", "5", "5-", "5+", "6"]

class GradeBase(BaseModel):
    """Podstawowy schemat oceny."""
    value: GradeValue = Field(..., description="Wartość oceny (np. 1, 2+, 4-)")
    weight: float = Field(1.0, ge=0, description="Waga oceny")
    description: Optional[str] = Field(None, description="Opis oceny")
    subject_id: int

class GradeCreate(GradeBase):
    """Schemat do tworzenia nowej oceny."""
    student_id: int

class GradeUpdate(BaseModel):
    """Schemat do aktualizacji oceny."""
    value: Optional[GradeValue] = None
    weight: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None

class Grade(GradeBase):
    """Pełny schemat oceny zwracany z bazy."""
    id: int
    student_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)