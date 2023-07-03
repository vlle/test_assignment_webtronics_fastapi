from models import Robot
from pydantic_models import RobotLoginForm, RobotUser
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


async def register_user(session: AsyncSession, robot_user: RobotUser):
    user = Robot(**robot_user.dict())
    session.add(user)
    await session.commit()


async def login_user(session: AsyncSession, robot_user: RobotLoginForm):
    stmt = select(Robot).where(
        and_(Robot.login == robot_user.login, Robot.password == robot_user.password)
    )
    print(2)
    async with session, session.begin():
        result = await session.scalars(stmt)
        return result.one_or_none()


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(Robot))
    return [row[0].login for row in result]
