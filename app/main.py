from authentication import KEY, authenticate_user, get_password_hash, has_access
from crud import (
    create_video,
    delete_video,
    get_video,
    like_video,
    register_user,
    update_video,
)
from database import engine, init_models, maker
from fastapi import Depends, FastAPI, HTTPException, status
from jose import jwt
from pydantic_models import RobotLoginForm, RobotUser, Video
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

application = FastAPI()


@application.on_event("startup")
async def init_db() -> None:
    await init_models(engine)


async def db_connection():
    db = maker()
    try:
        yield db
    finally:
        await db.close()


@application.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "User already exists"},
        status.HTTP_201_CREATED: {"description": "User created"},
    },
)
async def signup(user: RobotUser, db: AsyncSession = Depends(db_connection)):
    user.password = get_password_hash(user.password)
    try:
        await register_user(db, user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    return {"status": "success"}


@application.get(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Wrong login or password"},
        status.HTTP_200_OK: {"description": "User logged in"},
    },
)
async def login(login: str, password: str, db: AsyncSession = Depends(db_connection)):
    user = RobotLoginForm(login=login, password=password)
    authorized_user = await authenticate_user(db, user)
    if not authorized_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong login or password"
        )

    payload = {"user_id": authorized_user.id, "login": authorized_user.login}
    encoded = jwt.encode(payload, key=KEY)
    return {"token": encoded}


@application.post("/create_post", status_code=status.HTTP_201_CREATED)
async def create_post(
    video: Video,
    payload: dict = Depends(has_access),
    db: AsyncSession = Depends(db_connection),
):
    user_id = payload["user_id"]
    video_id = await create_video(db, video, user_id)
    return {"status": "success", "video_id": video_id}


@application.put("/edit_post", status_code=status.HTTP_200_OK)
async def edit_post(
    video_id: int,
    video: Video,
    payload: dict = Depends(has_access),
    db: AsyncSession = Depends(db_connection),
):
    user_id = payload["user_id"]
    status = await update_video(db, video, video_id, user_id)
    return {"status": "success" if status is True else "failed"}


@application.delete("/delete_post", status_code=status.HTTP_200_OK)
async def delete_post(
    video_id: int,
    payload: dict = Depends(has_access),
    db: AsyncSession = Depends(db_connection),
):
    user_id = payload["user_id"]
    status = await delete_video(db, video_id, user_id)
    return {"status": "success" if status is True else "failed"}


@application.get("/view_post")
async def view_post(video_id: int, db: AsyncSession = Depends(db_connection)):
    video = await get_video(db, video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    return {"video": Video(name=video.name, description=video.description)}


@application.post("/like_post")
async def like_post(
    video_id: int,
    payload: dict = Depends(has_access),
    db: AsyncSession = Depends(db_connection),
):
    user_id = payload["user_id"]
    video = await get_video(db, video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    if video.author == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't like your own video",
        )
    operation_status = await like_video(db, video_id, user_id)
    return {"status": "success" if operation_status is True else "failed"}


@application.post("/dislike_post")
async def dislike_post():
    return {"dislike_post": "dislike_post"}


@application.get("/get_likes")
async def get_likes(video_id: int, db: AsyncSession = Depends(db_connection)):
    video = await get_video(db, video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
    likes = video.likes
    return {"likes": likes}
