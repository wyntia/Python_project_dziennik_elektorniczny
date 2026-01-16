from fastapi import APIRouter, Depends
from app.api.routes import students, subjects, grades, teachers, remarks, reports, auth
from app.api.deps import get_current_user

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

router.include_router(
    students.router,
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    subjects.router,
    prefix="/subjects",
    tags=["Subjects"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    grades.router,
    prefix="/grades",
    tags=["Grades"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    teachers.router,
    prefix="/teachers",
    tags=["Teachers"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    remarks.router,
    prefix="/remarks",
    tags=["Remarks"],
    dependencies=[Depends(get_current_user)]
)

router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_user)]
)