from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas import Student, StudentCreate, StudentUpdate
from app.crud import crud_student

router = APIRouter()


@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    """Dodaje studenta. Sprawdza czy PESEL jest unikalny."""
    existing = await crud_student.get_student_by_pesel(db, student.pesel)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Uczeń z PESEL {student.pesel} już figuruje w bazie."
        )
    return await crud_student.create_student(db, student)


@router.get("/", response_model=List[Student])
async def list_students(db: AsyncSession = Depends(get_db)):
    """Wyświetla wszystkich uczniów."""
    return await crud_student.get_students(db)


@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Pobiera jednego ucznia."""
    s = await crud_student.get_student(db, student_id)
    if not s:
        raise HTTPException(status_code=404, detail="Student nie istnieje.")
    return s


@router.patch("/{student_id}", response_model=Student)
async def edit_student(student_id: int, student_data: StudentUpdate, db: AsyncSession = Depends(get_db)):
    """Edytuje dane ucznia."""
    if student_data.pesel:
        existing = await crud_student.get_student_by_pesel(db, student_data.pesel)
        if existing and existing.id != student_id:
            raise HTTPException(status_code=400, detail="Inny uczeń ma już ten PESEL.")

    res = await crud_student.update_student(db, student_id, student_data)
    if not res:
        raise HTTPException(status_code=404, detail="Nie znaleziono studenta.")
    return res


@router.delete("/{student_id}")
async def remove_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Usuwa ucznia."""
    if not await crud_student.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student nie istnieje.")
    return {"message": f"Uczeń o ID {student_id} został usunięty."}