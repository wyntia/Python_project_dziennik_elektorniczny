from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Subjects import Subject
from app.schemas import SubjectCreate, SubjectUpdate
from typing import List, Optional

async def get_subject(db: AsyncSession, subject_id: int) -> Optional[Subject]:
    """Pobiera jeden przedmiot na podstawie ID."""
    result = await db.execute(select(Subject).where(Subject.id == subject_id))
    return result.scalar_one_or_none()

async def get_subject_by_name(db: AsyncSession, name: str) -> Optional[Subject]:
    """Wyszukuje przedmiot po nazwie (do sprawdzania unikalności)."""
    result = await db.execute(select(Subject).where(Subject.name == name))
    return result.scalar_one_or_none()

async def get_subjects(db: AsyncSession) -> List[Subject]:
    """Pobiera wszystkie przedmioty z bazy."""
    result = await db.execute(select(Subject))
    return result.scalars().all()

async def create_subject(db: AsyncSession, subject: SubjectCreate) -> Subject:
    """Tworzy nowy przedmiot z opcjonalnym opisem."""
    db_subject = Subject(**subject.model_dump())
    db.add(db_subject)
    await db.commit()
    await db.refresh(db_subject)
    return db_subject

async def update_subject(db: AsyncSession, subject_id: int, subject_data: SubjectUpdate) -> Optional[Subject]:
    """Aktualizuje dane przedmiotu."""
    db_subject = await get_subject(db, subject_id)
    if not db_subject:
        return None

    update_data = subject_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subject, key, value)

    await db.commit()
    await db.refresh(db_subject)
    return db_subject

async def delete_subject(db: AsyncSession, subject_id: int) -> bool:
    """Usuwa przedmiot z bazy danych."""
    db_subject = await get_subject(db, subject_id)
    if db_subject:
        await db.delete(db_subject)
        await db.commit()
        return True
    return False