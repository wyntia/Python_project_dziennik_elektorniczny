from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Student import Student
from app.schemas import StudentCreate, StudentUpdate
from typing import List, Optional

async def get_student(db: AsyncSession, student_id: int) -> Optional[Student]:
    """Pobiera jednego ucznia na podstawie ID."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    return result.scalar_one_or_none()

async def get_student_by_pesel(db: AsyncSession, pesel: str) -> Optional[Student]:
    """Wyszukuje ucznia po numerze PESEL."""
    result = await db.execute(select(Student).where(Student.pesel == pesel))
    return result.scalar_one_or_none()

async def get_students(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Student]:
    """Pobiera listę wszystkich uczniów."""
    result = await db.execute(select(Student).offset(skip).limit(limit))
    return result.scalars().all()

async def create_student(db: AsyncSession, student: StudentCreate) -> Student:
    """Tworzy nowego ucznia w bazie danych."""
    db_student = Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

async def update_student(db: AsyncSession, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
    """Aktualizuje dane istniejącego ucznia."""
    db_student = await get_student(db, student_id)
    if not db_student:
        return None

    update_data = student_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    await db.commit()
    await db.refresh(db_student)
    return db_student

async def delete_student(db: AsyncSession, student_id: int) -> bool:
    """Usuwa ucznia z bazy."""
    db_student = await get_student(db, student_id)
    if db_student:
        await db.delete(db_student)
        await db.commit()
        return True
    return False