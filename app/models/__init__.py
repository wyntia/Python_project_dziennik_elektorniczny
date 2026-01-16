from app.db.session import Base
from app.models.Student import Student
from app.models.Subjects import Subject
from app.models.Grade import Grade
from app.models.Teacher import Teacher
from app.models.Remark import Remark

__all__ = ["Base", "Student", "Subject", "Grade", "Teacher", "Remark"]