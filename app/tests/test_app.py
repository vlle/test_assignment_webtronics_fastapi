import pytest
from crud import get_all_users
from fastapi.testclient import TestClient
from main import application
from models import Base
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

TEST_DB_URL = "sqlite+aiosqlite://"

engine = create_async_engine(TEST_DB_URL, echo=False)
maker = async_sessionmaker(engine, expire_on_commit=False)

client = TestClient(application)


async def drop_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
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
async def test_signup_robot(get_session):
    await drop_tables(engine)
    await create_tables(engine)
    session = await get_session
    response = client.post(
        url="/signup",
        json={"login": "test", "password": "test", "email": "test@yahoo.com"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert "test" in (await get_all_users(session))
