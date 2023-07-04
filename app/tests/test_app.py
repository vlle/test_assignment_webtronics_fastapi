import jwt
import pytest
from crud import get_all_users
from database import DATABASE_URL, MissingEnvironmentVariable
from httpx import AsyncClient
from main import KEY, application
from models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if not DATABASE_URL:
    raise MissingEnvironmentVariable("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
maker = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def table_creation():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def get_session():
    db = maker()
    try:
        yield db
    finally:
        await db.close()


@pytest.mark.asyncio
async def test_signup_robot(table_creation, get_session):
    await table_creation
    session = await anext(get_session)
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


@pytest.mark.asyncio
async def test_signup_robot_already_registered(table_creation, get_session):
    await table_creation
    session = await anext(get_session)
    assert "test" not in (await get_all_users(session))
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        response = await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert "test" in (await get_all_users(session))
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        response = await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
    assert response.status_code == 400
    await session.close()


@pytest.mark.asyncio
async def test_login_robot(table_creation):
    await table_creation
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        response_register = await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
        response_login = await ac.get(
            url="/login",
            params={"login": "test", "password": "test"},
        )
    assert response_register.status_code == 201
    assert response_login.status_code == 200
    assert response_login.json()["token"] is not None
    decoded = jwt.decode(response_login.json()["token"], KEY, algorithms=["HS256"])
    assert decoded["login"] == "test"
