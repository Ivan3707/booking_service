from datetime import datetime, timedelta

import pytest_asyncio
from sqlalchemy import text
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings
from src.main import app


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

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport,base_url="http://test",follow_redirects=True) as ac:
        yield ac

"""
import asyncio
import pytest_asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from httpx import AsyncClient, ASGITransport

from src.core.config import settings
from src.main import app


# =========================
# EVENT LOOP FIX (CRITICAL)
# =========================
import pytest

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# =========================
# ENGINE (shared per test function)
# =========================
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


# =========================
# SESSION MAKER
# =========================
@pytest_asyncio.fixture(scope="function")
def sessionmaker(engine):
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


# =========================
# DB SESSION (OPTIONAL USE)
# =========================
@pytest_asyncio.fixture
async def db_session(sessionmaker):
    async with sessionmaker() as session:
        yield session
        await session.rollback()


# =========================
# CLEANUP (FIXED + SAFE)
# =========================
@pytest_asyncio.fixture(autouse=True)
async def cleanup(sessionmaker):
    async with sessionmaker() as session:
        await _truncate_all(session)
    yield
    async with sessionmaker() as session:
        await _truncate_all(session)


async def _truncate_all(session: AsyncSession):
    # ВАЖНО: text() обязательно (SQLAlchemy 2.0 fix)
    await session.execute(text("TRUNCATE TABLE bookings CASCADE"))
    await session.execute(text("TRUNCATE TABLE slots CASCADE"))
    await session.execute(text("TRUNCATE TABLE schedules CASCADE"))
    await session.execute(text("TRUNCATE TABLE users CASCADE"))
    await session.execute(text("TRUNCATE TABLE rooms CASCADE"))
    await session.commit()


# =========================
# HTTP CLIENT (FASTAPI TESTING)
# =========================
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        follow_redirects=True,
    ) as ac:
        yield ac
"""