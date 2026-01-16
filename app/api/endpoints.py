from fastapi import APIRouter
from app.api.routes import students, subjects, grades

router = APIRouter()

router.include_router(students.router, prefix="/students", tags=["Students"])
router.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
router.include_router(grades.router, prefix="/grades", tags=["Grades"])