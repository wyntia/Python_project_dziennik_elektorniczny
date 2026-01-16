import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db.session import Base, get_db
from app.core.config import settings

TEST_DB_NAME = "test_school_db"
BASE_URL = settings.DATABASE_URL.rsplit('/', 1)[0]
TEST_DATABASE_URL = f"{BASE_URL}/{TEST_DB_NAME}"


@pytest.fixture(scope="session", autouse=True)
async def create_test_database():
    """Tworzy bazę danych testową, jeśli nie istnieje."""
    root_engine = create_async_engine(f"{BASE_URL}/mysql", isolation_level="AUTOCOMMIT")
    async with root_engine.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {TEST_DB_NAME}"))
    await root_engine.dispose()
    yield


@pytest.fixture(scope="session")
def event_loop():
    """Tworzy instancję pętli zdarzeń dla całej sesji testowej."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session():
    """
    Przygotowuje czyste tabele dla każdego testu.
    To jest fixture, której brakowało w Twoim błędzie.
    """
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)

    async with Session() as session:
        yield session

    await test_engine.dispose()


@pytest.fixture(scope="function")
async def client(db_session):
    """
    Tworzy klienta testowego i podmienia bazę danych na testową.
    Używa ASGITransport dla zgodności z httpx >= 0.21.0.
    """

    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def token_headers(client, db_session):
    """Pomocnicza fixture tworząca zalogowanego admina i zwracająca nagłówki."""
    from app.core.security import get_password_hash, create_access_token
    from app.models.User import User

    user = User(username="admin", hashed_password=get_password_hash("admin123"), is_active=True)
    db_session.add(user)
    await db_session.commit()

    token = create_access_token(subject="admin")
    return {"Authorization": f"Bearer {token}"}