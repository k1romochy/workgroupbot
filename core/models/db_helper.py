from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.models.base import Base

from dotenv import load_dotenv
import os

load_dotenv()
engine = create_async_engine(url=os.getenv('POSTGRES_URL'))

async_session = async_sessionmaker(engine)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
