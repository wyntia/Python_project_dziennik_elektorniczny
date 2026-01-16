from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Remark import Remark
from app.schemas import RemarkCreate, RemarkUpdate
from typing import List, Optional


async def create_remark(db: AsyncSession, remark: RemarkCreate) -> Remark:
    """
    Tworzy i zapisuje nową uwagę w bazie danych.
    """
    db_remark = Remark(**remark.model_dump())
    db.add(db_remark)
    await db.commit()
    await db.refresh(db_remark)
    return db_remark


async def get_student_remarks(db: AsyncSession, student_id: int) -> List[Remark]:
    """
    Pobiera listę wszystkich uwag przypisanych do konkretnego ucznia.
    """
    result = await db.execute(select(Remark).where(Remark.student_id == student_id))
    return result.scalars().all()


async def get_remark(db: AsyncSession, remark_id: int) -> Optional[Remark]:
    """
    Pobiera pojedynczą uwagę na podstawie jej unikalnego ID.
    """
    result = await db.execute(select(Remark).where(Remark.id == remark_id))
    return result.scalar_one_or_none()


async def update_remark(db: AsyncSession, remark_id: int, remark_data: RemarkUpdate) -> Optional[Remark]:
    """
    Aktualizuje treść lub punktację istniejącej uwagi.
    """
    db_remark = await get_remark(db, remark_id)
    if not db_remark:
        return None

    update_data = remark_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_remark, key, value)

    await db.commit()
    await db.refresh(db_remark)
    return db_remark


async def delete_remark(db: AsyncSession, remark_id: int) -> bool:
    """
    Trwale usuwa uwagę z bazy danych.
    """
    db_remark = await get_remark(db, remark_id)
    if db_remark:
        await db.delete(db_remark)
        await db.commit()
        return True
    return False