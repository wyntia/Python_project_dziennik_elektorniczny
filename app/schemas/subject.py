from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SubjectBase(BaseModel):
    """Podstawowy schemat przedmiotu."""
    name: str = Field(..., min_length=1, description="Nazwa przedmiotu")
    description: Optional[str] = Field(None, description="Opcjonalny opis przedmiotu")

class SubjectCreate(SubjectBase):
    """Schemat do tworzenia przedmiotu."""
    pass

class SubjectUpdate(BaseModel):
    """Schemat do aktualizacji przedmiotu."""
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None

class Subject(SubjectBase):
    """Pełny schemat przedmiotu zwracany z bazy."""
    id: int
    model_config = ConfigDict(from_attributes=True)