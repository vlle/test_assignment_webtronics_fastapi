from models import Robot, Video
from pydantic_models import RobotLoginForm, RobotUser
from pydantic_models import Video as VideoPydantic
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def register_user(session: AsyncSession, robot_user: RobotUser):
    user = Robot(**robot_user.dict())
    session.add(user)
    await session.commit()


async def get_user_by_login(session: AsyncSession, login: str) -> Robot | None:
    stmt = select(Robot).where(Robot.login == login)
    async with session, session.begin():
        result = await session.scalars(stmt)
        return result.one_or_none()


async def login_user(session: AsyncSession, robot_user: RobotLoginForm) -> Robot | None:
    stmt = select(Robot).where(
        and_(Robot.login == robot_user.login, Robot.password == robot_user.password)
    )
    async with session, session.begin():
        result = await session.scalars(stmt)
        return result.one_or_none()


async def create_video(
    session: AsyncSession, video: VideoPydantic, user_id: int
) -> int:
    video = Video(**video.dict())
    video.author = user_id
    session.add(video)
    await session.commit()
    return video.id


async def get_video(session: AsyncSession, video_id: int) -> Video | None:
    stmt = select(Video).options(selectinload(Video.likes)).where(Video.id == video_id)
    async with session, session.begin():
        result = await session.scalars(stmt)
        return result.one_or_none()


async def update_video(
    session: AsyncSession, video_inc: VideoPydantic, video_id: int, author_id: int
) -> int:
    stmt = select(Video).where(and_(Video.id == video_id, Video.author == author_id))
    async with session, session.begin():
        result = await session.scalars(stmt)
        video = result.one_or_none()
        if video:
            video.name = video_inc.name
            video.description = video_inc.description
            session.add(video)
            await session.commit()
            return True
        return False


async def like_video(session: AsyncSession, video_id: int, author_id: int) -> int:
    stmt = select(Video).options(selectinload(Video.likes)).where(Video.id == video_id)
    async with session, session.begin():
        result = await session.scalars(stmt)
        video = result.one_or_none()
        if video:
            video.likes.append(await session.get(Robot, author_id))
            session.add(video)
            await session.commit()
            return True
        return False


async def dislike_video(session: AsyncSession, video_id: int, author_id: int) -> int:
    stmt = select(Video).options(selectinload(Video.likes)).where(Video.id == video_id)
    async with session, session.begin():
        result = await session.scalars(stmt)
        video = result.one_or_none()
        if video:
            video.likes.remove(await session.get(Robot, author_id))
            session.add(video)
            await session.commit()
            return True
        return False


async def delete_video(session: AsyncSession, video_id: int, author_id: int) -> int:
    stmt = select(Video).where(and_(Video.id == video_id, Video.author == author_id))
    async with session, session.begin():
        result = await session.scalars(stmt)
        video = result.one_or_none()
        if video:
            await session.delete(video)
            await session.commit()
            return True
        return False


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(Robot))
    return [row[0].login for row in result]
