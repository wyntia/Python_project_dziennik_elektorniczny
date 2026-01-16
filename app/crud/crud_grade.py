from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Grade import Grade
from app.schemas import GradeCreate, GradeUpdate
from typing import List, Optional

async def get_grade(db: AsyncSession, grade_id: int) -> Optional[Grade]:
    """Pobiera pojedynczą ocenę po ID."""
    result = await db.execute(select(Grade).where(Grade.id == grade_id))
    return result.scalar_one_or_none()

async def create_grade(db: AsyncSession, grade: GradeCreate) -> Grade:
    """Zapisuje nową ocenę w bazie danych."""
    db_grade = Grade(**grade.model_dump())
    db.add(db_grade)
    await db.commit()
    await db.refresh(db_grade)
    return db_grade

async def get_student_grades(db: AsyncSession, student_id: int) -> List[Grade]:
    """Pobiera wszystkie oceny przypisane do konkretnego ucznia."""
    result = await db.execute(select(Grade).where(Grade.student_id == student_id))
    return result.scalars().all()

async def update_grade(db: AsyncSession, grade_id: int, grade_data: GradeUpdate) -> Optional[Grade]:
    """Aktualizuje dane oceny."""
    db_grade = await get_grade(db, grade_id)
    if not db_grade:
        return None

    update_data = grade_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_grade, key, value)

    await db.commit()
    await db.refresh(db_grade)
    return db_grade

async def delete_grade(db: AsyncSession, grade_id: int) -> bool:
    """Usuwa ocenę z bazy danych."""
    db_grade = await get_grade(db, grade_id)
    if db_grade:
        await db.delete(db_grade)
        await db.commit()
        return True
    return False