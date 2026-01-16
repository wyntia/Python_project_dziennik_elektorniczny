from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas import Grade, GradeCreate, GradeUpdate
from app.crud import crud_grade

router = APIRouter()

@router.post("/", response_model=Grade, status_code=status.HTTP_201_CREATED)
async def add_grade(grade: GradeCreate, db: AsyncSession = Depends(get_db)):
    """Wystawia nową ocenę."""
    return await crud_grade.create_grade(db, grade)

@router.get("/student/{student_id}", response_model=List[Grade])
async def get_student_grades(student_id: int, db: AsyncSession = Depends(get_db)):
    """Zwraca listę wszystkich ocen danego ucznia."""
    return await crud_grade.get_student_grades(db, student_id)

@router.patch("/{grade_id}", response_model=Grade)
async def edit_grade(grade_id: int, grade_data: GradeUpdate, db: AsyncSession = Depends(get_db)):
    """Umożliwia poprawienie oceny, zmianę jej wagi lub opisu."""
    updated = await crud_grade.update_grade(db, grade_id, grade_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Ocena nie istnieje.")
    return updated

@router.delete("/{grade_id}")
async def delete_grade(grade_id: int, db: AsyncSession = Depends(get_db)):
    """Usuwa ocenę i zwraca komunikat potwierdzający."""
    if not await crud_grade.delete_grade(db, grade_id):
        raise HTTPException(status_code=404, detail="Nie znaleziono oceny o tym ID.")
    return {"message": f"Ocena o ID {grade_id} została pomyślnie usunięty."}