"""
Pakiet zawierający wszystkie schematy Pydantic używane w aplikacji.
Eksportuje klasy z poszczególnych modułów dla łatwiejszego dostępu.
"""
from .student import Student, StudentCreate, StudentUpdate
from .subject import Subject, SubjectCreate, SubjectUpdate
from .grade import Grade, GradeCreate, GradeUpdate
from .teacher import Teacher, TeacherCreate, TeacherUpdate
from .remark import Remark, RemarkCreate, RemarkUpdate

__all__ = [
    "Student", "StudentCreate", "StudentUpdate",
    "Subject", "SubjectCreate", "SubjectUpdate",
    "Grade", "GradeCreate", "GradeUpdate",
    "Teacher", "TeacherCreate", "TeacherUpdate",
    "Remark", "RemarkCreate", "RemarkUpdate",
]