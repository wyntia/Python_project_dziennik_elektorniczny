from pydantic import BaseModel, ConfigDict, Field
from typing import List, Literal, Optional
from datetime import date
from .grade import Grade

class StudentBase(BaseModel):
    """Podstawowe dane ucznia."""
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    birth_date: date
    gender: Literal["kobieta", "mężczyzna"]
    pesel: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")

class StudentCreate(StudentBase):
    """Schemat do rejestracji ucznia."""
    pass

class StudentUpdate(BaseModel):
    """Schemat do edycji danych ucznia."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Literal["kobieta", "mężczyzna"]] = None
    pesel: Optional[str] = Field(None, min_length=11, max_length=11, pattern=r"^\d{11}$")

class Student(StudentBase):
    """Pełny schemat ucznia z listą ocen."""
    id: int
    grades: List[Grade] = []
    model_config = ConfigDict(from_attributes=True)