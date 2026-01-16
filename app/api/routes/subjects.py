from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas import Subject, SubjectCreate, SubjectUpdate
from app.crud import crud_subject

router = APIRouter()

@router.post("/", response_model=Subject, status_code=status.HTTP_201_CREATED)
async def create_new_subject(subject: SubjectCreate, db: AsyncSession = Depends(get_db)):
    """Dodaje nowy przedmiot. Sprawdza, czy nazwa nie jest duplikatem."""
    existing = await crud_subject.get_subject_by_name(db, name=subject.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Przedmiot o nazwie '{subject.name}' już istnieje w systemie."
        )
    return await crud_subject.create_subject(db, subject)

@router.get("/", response_model=List[Subject])
async def read_subjects(db: AsyncSession = Depends(get_db)):
    """Pobiera listę wszystkich przedmiotów."""
    return await crud_subject.get_subjects(db)

@router.get("/{subject_id}", response_model=Subject)
async def read_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    """Pobiera pojedynczy przedmiot po ID."""
    subject = await crud_subject.get_subject(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Przedmiot nie istnieje.")
    return subject

@router.patch("/{subject_id}", response_model=Subject)
async def update_subject(subject_id: int, subject_data: SubjectUpdate, db: AsyncSession = Depends(get_db)):
    """Aktualizuje dane przedmiotu. Weryfikuje unikalność przy zmianie nazwy."""
    if subject_data.name:
        existing = await crud_subject.get_subject_by_name(db, name=subject_data.name)
        if existing and existing.id != subject_id:
            raise HTTPException(
                status_code=400,
                detail=f"Inny przedmiot o nazwie '{subject_data.name}' już istnieje."
            )

    updated = await crud_subject.update_subject(db, subject_id, subject_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Nie znaleziono przedmiotu do edycji.")
    return updated

@router.delete("/{subject_id}")
async def delete_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    """
    Usuwa przedmiot z bazy.
    Zwraca wiadomość zwrotną po pomyślnym usunięciu.
    """
    success = await crud_subject.delete_subject(db, subject_id)
    if not success:
        raise HTTPException(status_code=404, detail="Przedmiot nie został znaleziony.")
    return {"message": f"Przedmiot o ID {subject_id} został pomyślnie usunięty."}