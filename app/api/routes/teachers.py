from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas import Teacher, TeacherCreate, TeacherUpdate
from app.crud import crud_teacher

router = APIRouter()


@router.post("/", response_model=Teacher, status_code=status.HTTP_201_CREATED)
async def add_teacher(teacher: TeacherCreate, db: AsyncSession = Depends(get_db)) -> Teacher:
    """
    Endpoint do dodawania nowego nauczyciela.
    Sprawdza unikalność numeru PESEL.
    """
    existing = await crud_teacher.get_teacher_by_pesel(db, teacher.pesel)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nauczyciel z tym PESEL już istnieje."
        )
    return await crud_teacher.create_teacher(db, teacher)


@router.get("/", response_model=List[Teacher])
async def list_teachers(db: AsyncSession = Depends(get_db)) -> List[Teacher]:
    """
    Pobiera listę wszystkich nauczycieli zarejestrowanych w systemie.
    """
    return await crud_teacher.get_teachers(db)


@router.patch("/{teacher_id}", response_model=Teacher)
async def edit_teacher(
        teacher_id: int,
        data: TeacherUpdate,
        db: AsyncSession = Depends(get_db)
) -> Teacher:
    """
    Aktualizuje dane nauczyciela o podanym ID.
    Weryfikuje unikalność numeru PESEL przy zmianie.
    """
    if data.pesel:
        existing = await crud_teacher.get_teacher_by_pesel(db, data.pesel)
        if existing and existing.id != teacher_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Podany PESEL jest już przypisany do innego nauczyciela."
            )

    res = await crud_teacher.update_teacher(db, teacher_id, data)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono nauczyciela.")
    return res


@router.delete("/{teacher_id}")
async def remove_teacher(teacher_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Usuwa nauczyciela z bazy danych na podstawie ID.
    """
    if not await crud_teacher.delete_teacher(db, teacher_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nauczyciel nie istnieje.")
    return {"message": f"Nauczyciel o ID {teacher_id} został pomyślnie usunięty."}


@router.post("/{teacher_id}/assign/{subject_id}")
async def assign_to_subject(teacher_id: int, subject_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Przypisuje nauczyciela do konkretnego przedmiotu szkolnego.
    """
    success = await crud_teacher.assign_teacher_to_subject(db, teacher_id, subject_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nie znaleziono nauczyciela lub przedmiotu."
        )
    return {"message": "Nauczyciel został pomyślnie przypisany do przedmiotu."}