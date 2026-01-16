# from pydantic import BaseModel, ConfigDict, Field
# from typing import List, Literal, Optional
# from datetime import date, datetime
#
# GradeValue = Literal["1", "2-", "2+", "3-", "3+", "4", "4-", "4+", "5", "5-", "5+", "6"]
#
# class GradeBase(BaseModel):
#     value: GradeValue = Field(..., description="Wartość oceny (np. 1, 2+, 4-)")
#     weight: float = Field(1.0, ge=0, description="Waga oceny")
#     description: Optional[str] = Field(None, description="Opis (np. Sprawdzian z ułamków)")
#     subject_id: int
#
# class GradeCreate(GradeBase):
#     student_id: int
#
# class GradeUpdate(BaseModel):
#     """Schemat do edycji oceny."""
#     value: Optional[GradeValue] = None
#     weight: Optional[float] = Field(None, ge=0)
#     description: Optional[str] = None
#
# class Grade(GradeBase):
#     id: int
#     student_id: int
#     created_at: datetime
#     model_config = ConfigDict(from_attributes=True)
#
# class SubjectBase(BaseModel):
#     name: str = Field(..., min_length=1, description="Nazwa przedmiotu")
#     description: Optional[str] = Field(None, description="Opcjonalny opis przedmiotu")
#
# class SubjectCreate(SubjectBase):
#     pass
#
# class SubjectUpdate(BaseModel):
#     """Schemat do aktualizacji przedmiotu - wszystkie pola są opcjonalne."""
#     name: Optional[str] = Field(None, min_length=1)
#     description: Optional[str] = None
#
# class Subject(SubjectBase):
#     id: int
#     model_config = ConfigDict(from_attributes=True)
#
# class StudentBase(BaseModel):
#     first_name: str = Field(..., min_length=1)
#     last_name: str = Field(..., min_length=1)
#     birth_date: date
#     gender: Literal["kobieta", "mężczyzna"]
#     pesel: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")
#
# class StudentCreate(StudentBase):
#     pass
#
# class StudentUpdate(BaseModel):
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     birth_date: Optional[date] = None
#     gender: Optional[Literal["kobieta", "mężczyzna"]] = None
#     pesel: Optional[str] = Field(None, min_length=11, max_length=11, pattern=r"^\d{11}$")
#
# class Student(StudentBase):
#     id: int
#     grades: List[Grade] = []
#     model_config = ConfigDict(from_attributes=True)