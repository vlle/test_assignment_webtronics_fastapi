from models import Robot
from pydantic_models import RobotUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def register_user(session: AsyncSession, robot_user: RobotUser):
    user = Robot(**robot_user.dict())
    session.add(user)
    await session.commit()


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(Robot))
    return [row[0].login for row in result]
