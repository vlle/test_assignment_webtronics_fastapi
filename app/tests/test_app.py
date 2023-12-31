import pytest
from crud import get_all_users
from database import DATABASE_URL, MissingEnvironmentVariable
from httpx import AsyncClient
from jose import jwt
from main import KEY, application
from models import Base, Video
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
    password = login = "test"
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        response_register = await ac.post(
            url="/signup",
            json={"login": login, "password": password, "email": "test@yahoo.com"},
        )
        response_login = await ac.get(
            url="/login",
            params={"login": login, "password": password},
        )
    assert response_register.status_code == 201
    assert response_login.status_code == 200
    assert response_login.json()["token"] is not None
    decoded = jwt.decode(response_login.json()["token"], KEY, algorithms=["HS256"])
    assert decoded["login"] == "test"


@pytest.mark.asyncio
async def test_create_video(table_creation):
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
        token = response_login.json()["token"]
        response_create_video = await ac.post(
            url="/create_post",
            json={"name": "test", "description": "test"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response_create_video.status_code == 201


@pytest.mark.asyncio
async def test_get_video(table_creation):
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
        token = response_login.json()["token"]
        response_create_video = await ac.post(
            url="/create_post",
            json={"name": "test", "description": "test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        video_id = response_create_video.json()["video_id"]
        response_get_video = await ac.get(
            url=f"/view_post/{video_id}",
        )
        assert response_get_video.status_code == 200
        assert response_get_video.json()["video"]["name"] == "test"


@pytest.mark.asyncio
async def test_get_not_exists_video(table_creation):
    await table_creation
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        response_get_video = await ac.get(
            url="/view_post/-1",
        )
        assert response_get_video.status_code == 404


@pytest.mark.asyncio
async def test_edit_video(table_creation):
    await table_creation
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
        login = await ac.get(
            url="/login",
            params={"login": "test", "password": "test"},
        )
        token = login.json()["token"]
        response_create_video = await ac.post(
            url="/create_post",
            json={"name": "test", "description": "test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        video_id = response_create_video.json()["video_id"]
        response_edit_video = await ac.put(
            url=f"/edit_post/{video_id}",
            json={"name": "test2", "description": "description"},
            headers={"Authorization": f"Bearer {token}"},
        )
        print(response_edit_video.json())
        assert response_edit_video.status_code == 200
        assert response_edit_video.json()["status"] == "success"

        response_get_video = await ac.get(
            url=f"/view_post/{video_id}",
        )
        assert response_get_video.status_code == 200
        assert response_get_video.json()["video"]["name"] == "test2"


@pytest.mark.asyncio
async def test_delete_video(table_creation):
    await table_creation
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
        login = await ac.get(
            url="/login",
            params={"login": "test", "password": "test"},
        )
        token = login.json()["token"]
        response_create_video = await ac.post(
            url="/create_post",
            json={"name": "test", "description": "test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        video_id = response_create_video.json()["video_id"]

        response_get_video = await ac.get(
            url=f"/view_post/{video_id}",
        )
        assert response_get_video.status_code == 200
        response_delete_video = await ac.delete(
            url=f"/delete_post/{video_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response_delete_video.status_code == 200
        response_get_video = await ac.get(url=f"/view_post/{video_id}")
        assert response_get_video.status_code == 404


@pytest.mark.asyncio
async def test_like_video(table_creation):
    await table_creation
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
        login = await ac.get(
            url="/login",
            params={"login": "test", "password": "test"},
        )
        token = login.json()["token"]
        response_create_video = await ac.post(
            url="/create_post",
            json={"name": "test", "description": "test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        video_id = response_create_video.json()["video_id"]

        await ac.post(
            url="/signup",
            json={
                "login": "another_test",
                "password": "test",
                "email": "test2@yahoo.com",
            },
        )
        login = await ac.get(
            url="/login",
            params={"login": "another_test", "password": "test"},
        )
        token = login.json()["token"]
        response_like_video = await ac.post(
            url=f"/like_post/{video_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response_like_video.status_code == 200
        assert response_like_video.json()["status"] == "success"
        response_check_likes = await ac.get(
            url=f"/get_likes/{video_id}",
        )
        assert response_check_likes.status_code == 200
        assert len(response_check_likes.json()["likes"]) == 1


@pytest.mark.asyncio
async def test_dislike_video(table_creation):
    await table_creation
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
        login = await ac.get(
            url="/login",
            params={"login": "test", "password": "test"},
        )
        token = login.json()["token"]
        response_create_video = await ac.post(
            url="/create_post",
            json={"name": "test", "description": "test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        video_id = response_create_video.json()["video_id"]

        await ac.post(
            url="/signup",
            json={
                "login": "another_test",
                "password": "test",
                "email": "test2@yahoo.com",
            },
        )
        login = await ac.get(
            url="/login",
            params={"login": "another_test", "password": "test"},
        )
        token = login.json()["token"]
        response_like_video = await ac.post(
            url=f"/like_post/{video_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response_like_video.status_code == 200
        assert response_like_video.json()["status"] == "success"
        response_check_likes = await ac.get(
            url=f"/get_likes/{video_id}",
        )
        assert response_check_likes.status_code == 200
        assert len(response_check_likes.json()["likes"]) == 1

        response_dislike_video = await ac.post(
            url=f"/dislike_post/{video_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response_dislike_video.status_code == 200
        assert response_dislike_video.json()["status"] == "success"
        response_check_likes = await ac.get(
            url=f"/get_likes/{video_id}",
        )
        assert response_check_likes.status_code == 200
        assert len(response_check_likes.json()["likes"]) == 0


@pytest.mark.asyncio
async def test_is_author_can_like_own_video(table_creation):
    await table_creation
    async with AsyncClient(app=application, base_url="http://127.0.0.1") as ac:
        await ac.post(
            url="/signup",
            json={"login": "test", "password": "test", "email": "test@yahoo.com"},
        )
        login = await ac.get(
            url="/login",
            params={"login": "test", "password": "test"},
        )
        token = login.json()["token"]
        response_create_video = await ac.post(
            url="/create_post",
            json={"name": "test", "description": "test"},
            headers={"Authorization": f"Bearer {token}"},
        )
        video_id = response_create_video.json()["video_id"]
        response_like_video = await ac.post(
            url=f"/like_post/{video_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response_like_video.status_code == 400
