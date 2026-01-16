from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from .remark import Remark
from .subject import Subject


class TeacherBase(BaseModel):
    """
    Podstawowy schemat danych nauczyciela używany do współdzielenia pól.
    """
    first_name: str = Field(..., min_length=1, description="Imię nauczyciela")
    last_name: str = Field(..., min_length=1, description="Nazwisko nauczyciela")
    academic_degree: str = Field(..., min_length=2, description="Stopień naukowy (np. mgr)")
    pesel: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$", description="Numer PESEL")


class TeacherCreate(TeacherBase):
    """
    Schemat używany przy tworzeniu nowego nauczyciela w systemie.
    """
    pass


class TeacherUpdate(BaseModel):
    """
    Schemat używany do aktualizacji danych nauczyciela. Wszystkie pola są opcjonalne.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    academic_degree: Optional[str] = None
    pesel: Optional[str] = Field(None, min_length=11, max_length=11, pattern=r"^\d{11}$")


class Teacher(TeacherBase):
    """
    Pełny schemat nauczyciela zwracany przez API, zawierający ID oraz listę przedmiotów.
    """
    id: int
    subjects: List[Subject] = []
    remarks: List[Remark] = []

    model_config = ConfigDict(from_attributes=True)