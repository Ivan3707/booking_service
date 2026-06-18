import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings


@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def sessionmaker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def db_session(sessionmaker):
    async with sessionmaker() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture(autouse=True)
async def cleanup(db_session):
    yield

    async with db_session.begin():
        await db_session.execute(text("TRUNCATE users CASCADE"))
        await db_session.execute(text("TRUNCATE bookings CASCADE"))
        await db_session.execute(text("TRUNCATE slots CASCADE"))
        await db_session.execute(text("TRUNCATE schedules CASCADE"))
        await db_session.execute(text("TRUNCATE rooms CASCADE"))

