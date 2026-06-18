import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings


# -----------------------------
# ENGINE (per test function lifecycle SAFE)
# -----------------------------
@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    try:
        yield engine
    finally:
        await engine.dispose()


# -----------------------------
# SESSIONMAKER
# -----------------------------
@pytest_asyncio.fixture(scope="function")
def sessionmaker(engine):
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


# -----------------------------
# CLEAN DATABASE (IMPORTANT FIX)
# -----------------------------
@pytest_asyncio.fixture(autouse=True)
async def cleanup(sessionmaker):
    """
    ВАЖНО:
    чистим БД ДО И ПОСЛЕ теста
    чтобы избежать leakage между тестами
    """

    async with sessionmaker() as session:
        await session.execute(text("TRUNCATE bookings CASCADE"))
        await session.execute(text("TRUNCATE slots CASCADE"))
        await session.execute(text("TRUNCATE schedules CASCADE"))
        await session.execute(text("TRUNCATE users CASCADE"))
        await session.execute(text("TRUNCATE rooms CASCADE"))
        await session.commit()

    yield

    async with sessionmaker() as session:
        await session.execute(text("TRUNCATE bookings CASCADE"))
        await session.execute(text("TRUNCATE slots CASCADE"))
        await session.execute(text("TRUNCATE schedules CASCADE"))
        await session.execute(text("TRUNCATE users CASCADE"))
        await session.execute(text("TRUNCATE rooms CASCADE"))
        await session.commit()


# -----------------------------
# OPTIONAL: RAW DB SESSION (если нужен)
# -----------------------------
@pytest_asyncio.fixture
async def db_session(sessionmaker):
    async with sessionmaker() as session:
        yield session