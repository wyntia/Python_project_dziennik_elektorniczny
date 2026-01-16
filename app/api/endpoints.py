from fastapi import APIRouter
from app.api.routes import students, subjects, grades, teachers, remarks, reports

router = APIRouter()

router.include_router(students.router, prefix="/students", tags=["Students"])
router.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
router.include_router(grades.router, prefix="/grades", tags=["Grades"])
router.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
router.include_router(remarks.router, prefix="/remarks", tags=["Remarks"])
router.include_router(reports.router, prefix="/reports", tags=["Reports"])