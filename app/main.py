from crud import login_user, register_user
from database import engine, init_models, maker
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic_models import RobotLoginForm, RobotUser
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


# def signup
@application.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "User already exists"},
        status.HTTP_201_CREATED: {"description": "User created"},
    },
)
async def signup(user: RobotUser, db: AsyncSession = Depends(db_connection)):
    try:
        await register_user(db, user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    return {"status": "success"}


# def login
@application.get(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Wrong login or password"},
        status.HTTP_200_OK: {"description": "User logged in"},
    },
)
async def login(login: str, password: str, db: AsyncSession = Depends(db_connection)):
    print(1)
    user = RobotLoginForm(login=login, password=password)
    is_there_user = await login_user(db, user)
    if is_there_user:
        return {"status": "success"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong login or password"
        )


# def create_post
@application.post("/create_post")
async def create_post():
    return {"create_post": "create_post"}


# def edit_post
@application.put("/edit_post")
async def edit_post():
    return {"edit_post": "edit_post"}


# def delete_post
@application.delete("/delete_post")
async def delete_post():
    return {"delete_post": "delete_post"}


# def view_post
@application.get("/view_post")
async def view_post():
    return {"view_post": "view_post"}


# def like_post
@application.put("/like_post")
async def like_post():
    return {"like_post": "like_post"}


# def dislike_post
@application.put("/dislike_post")
async def dislike_post():
    return {"dislike_post": "dislike_post"}


# Description
# 	Create a simple RESTful API using FastAPI for a social networking application
# Functional requirements:
# There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
# As a user I need to be able to signup and login
# As a user I need to be able to create, edit, delete and view posts
# As a user I can like or dislike other users’ posts but not my own
# The API needs a UI Documentation (Swagger/ReDoc)
