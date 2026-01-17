from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.Teacher import Teacher
from app.models.Subjects import Subject
from app.schemas import TeacherCreate, TeacherUpdate
from typing import List, Optional


async def get_teacher(db: AsyncSession, teacher_id: int) -> Optional[Teacher]:
    """ Pobiera dane konkretnego nauczyciela z bazy danych na podstawie jego unikalnego identyfikatora ID. """
    return await db.get(Teacher, teacher_id)


async def get_teacher_by_pesel(db: AsyncSession, pesel: str) -> Optional[Teacher]:
    """ Pobiera dane konkretnego nauczyciela z bazy danych na podstawie jego numeru PESEL. """
    result = await db.execute(select(Teacher).where(Teacher.pesel == pesel))
    return result.scalar_one_or_none()


async def get_teachers(db: AsyncSession) -> List[Teacher]:
    """ Pobiera listę wszystkich nauczycieli z bazy danych. """
    result = await db.execute(select(Teacher))
    return result.scalars().all()


async def create_teacher(db: AsyncSession, teacher: TeacherCreate) -> Teacher:
    """ Tworzy nowego nauczyciela w bazie danych na podstawie dostarczonych danych. """
    db_teacher = Teacher(**teacher.model_dump())
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)
    return db_teacher


async def update_teacher(db: AsyncSession, teacher_id: int, teacher_data: TeacherUpdate) -> Optional[Teacher]:
    """ Aktualizuje dane istniejącego nauczyciela w bazie danych na podstawie dostarczonych danych. """
    db_teacher = await get_teacher(db, teacher_id)
    if not db_teacher:
        return None
    for key, value in teacher_data.model_dump(exclude_unset=True).items():
        setattr(db_teacher, key, value)
    await db.commit()
    await db.refresh(db_teacher)
    return db_teacher


async def delete_teacher(db: AsyncSession, teacher_id: int) -> bool:
    """ Usuwa nauczyciela z bazy danych na podstawie jego unikalnego identyfikatora ID. """
    db_teacher = await get_teacher(db, teacher_id)
    if db_teacher:
        await db.delete(db_teacher)
        await db.commit()
        return True
    return False


async def assign_teacher_to_subject(db: AsyncSession, teacher_id: int, subject_id: int) -> bool:
    """ Przypisuje nauczyciela do konkretnego przedmiotu na podstawie ich unikalnych identyfikatorów ID. """
    teacher = await get_teacher(db, teacher_id)
    result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = result.scalar_one_or_none()

    if teacher and subject:
        if subject not in teacher.subjects:
            teacher.subjects.append(subject)
            await db.commit()
            return True
    return False