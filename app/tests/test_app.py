import pytest
from crud import get_all_users
from database import DATABASE_URL, MissingEnvironmentVariable
from httpx import AsyncClient
from main import application
from models import Base
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

if not DATABASE_URL:
    raise MissingEnvironmentVariable("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
maker = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def table_creation():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def override_get_db():
    db = maker()
    try:
        yield db
    finally:
        await db.close()


@pytest.fixture
async def get_session():
    obj = override_get_db()
    session = await anext(obj)
    return session


@pytest.mark.asyncio
async def test_signup_robot(table_creation, get_session):
    await table_creation
    session = await get_session
    assert "test" not in (await get_all_users(session))
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        response = await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert "test" in (await get_all_users(session))
    await session.close()
