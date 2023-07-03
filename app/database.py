import os

from dotenv import load_dotenv
from models import Base
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


class MissingEnvironmentVariable(Exception):
    pass


async def init_models(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise MissingEnvironmentVariable

engine = create_async_engine(DATABASE_URL, echo=True)
maker = async_sessionmaker(engine, expire_on_commit=False)
