from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas import schemas
from app.crud import crud_student

router = APIRouter()


@router.post("/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
async def create_new_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    """Dodaje nowego ucznia. Waliduje unikalność PESEL."""
    existing = await crud_student.get_student_by_pesel(db, pesel=student.pesel)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Uczeń z numerem PESEL {student.pesel} już istnieje."
        )
    return await crud_student.create_student(db=db, student=student)


@router.get("/", response_model=List[schemas.Student])
async def read_all_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Zwraca listę wszystkich uczniów."""
    return await crud_student.get_students(db, skip=skip, limit=limit)


@router.get("/{student_id}", response_model=schemas.Student)
async def read_single_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """Pobiera dane jednego ucznia na podstawie ID."""
    student = await crud_student.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Nie znaleziono ucznia o podanym ID.")
    return student


@router.patch("/{student_id}", response_model=schemas.Student)
async def update_student_info(student_id: int, student_data: schemas.StudentUpdate, db: AsyncSession = Depends(get_db)):
    """Aktualizuje wybrane dane ucznia."""
    # Jeśli zmieniany jest PESEL, sprawdź czy nowy nie jest już zajęty
    if student_data.pesel:
        existing = await crud_student.get_student_by_pesel(db, pesel=student_data.pesel)
        if existing and existing.id != student_id:
            raise HTTPException(status_code=400, detail="Ten numer PESEL jest już przypisany do innego ucznia.")

    updated_student = await crud_student.update_student(db, student_id, student_data)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Nie można zaktualizować - uczeń nie istnieje.")
    return updated_student


@router.delete("/{student_id}")
async def remove_student(student_id: int, db: AsyncSession = Depends(get_db)):
    """
    Trwale usuwa ucznia z bazy danych.
    Zwraca wiadomość zwrotną po pomyślnym usunięciu.
    """
    success = await crud_student.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student nie znaleziony.")
    return {"message": f"Uczeń o ID {student_id} został pomyślnie usunięty z systemu."}