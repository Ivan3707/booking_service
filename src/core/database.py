from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import settings

# 1. Создаем асинхронный движок (Engine)
# Пул соединений (pool_size) позволяет держать открытыми несколько коннектов к БД,
# чтобы не тратить время на установку соединения при каждом запросе (критично для 100 RPS).
engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,          # Поставь True, если захочешь видеть чистый SQL-код в терминале
    pool_size=10,        # Сколько соединений держать открытыми
    max_overflow=20,     # Сколько соединений можно создать сверх пула при пиковой нагрузке
    isolation_level="SERIALIZABLE",
)

# 2. Создаем фабрику сессий (sessionmaker)
# expire_on_commit=False нужно для асинхронности, чтобы объекты не "пропадали" после коммита
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 3. Главная фишка: Асинхронный генератор зависимостей (Dependency)
# Этот инструмент будет выдавать сессию для каждого запроса и автоматически закрывать её
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()