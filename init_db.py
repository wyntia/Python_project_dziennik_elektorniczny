import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.User import User
from app.core.security import get_password_hash


async def init_admin():
    """
    Tworzy użytkownika admin z poprawnym haszem w bazie MySQL.
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.username == "admin"))
        user = result.scalar_one_or_none()

        if user:
            await db.delete(user)
            await db.commit()
            print("Zresetowano starego użytkownika admin.")

        new_user = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        db.add(new_user)
        await db.commit()
        print("Pomyślnie utworzono użytkownika: admin / admin123")


if __name__ == "__main__":
    asyncio.run(init_admin())