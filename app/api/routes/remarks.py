from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas import Remark, RemarkCreate, RemarkUpdate
from app.crud import crud_remark

router = APIRouter()

@router.post("/", response_model=Remark, status_code=status.HTTP_201_CREATED)
async def add_remark(remark: RemarkCreate, db: AsyncSession = Depends(get_db)):
    """
    Wystawia nową uwagę uczniowi przez nauczyciela.
    """
    return await crud_remark.create_remark(db, remark)

@router.get("/student/{student_id}", response_model=List[Remark])
async def read_student_remarks(student_id: int, db: AsyncSession = Depends(get_db)):
    """
    Zwraca listę wszystkich uwag przypisanych do danego ucznia.
    """
    return await crud_remark.get_student_remarks(db, student_id)

@router.patch("/{remark_id}", response_model=Remark)
async def edit_remark(remark_id: int, remark_data: RemarkUpdate, db: AsyncSession = Depends(get_db)):
    """
    Umożliwia zmianę punktacji lub opisu uwagi.
    """
    updated = await crud_remark.update_remark(db, remark_id, remark_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Uwaga nie została znaleziona.")
    return updated

@router.delete("/{remark_id}")
async def remove_remark(remark_id: int, db: AsyncSession = Depends(get_db)):
    """
    Usuwa uwagę i zwraca komunikat potwierdzający operację.
    """
    if not await crud_remark.delete_remark(db, remark_id):
        raise HTTPException(status_code=404, detail="Nie można usunąć - uwaga nie istnieje.")
    return {"message": f"Uwaga o ID {remark_id} została pomyślnie usunięta."}