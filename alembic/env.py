import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from src.core.config import settings

# 1. Импортируем наш Base и модели
from src.models.models import Base

# Это стандартная настройка логирования из файла конфигурации.
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Указываем target_metadata для автогенерации миграций
target_metadata = Base.metadata

# 3. Указываем URL нашей базы данных жестко (или можно брать из env)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме (без живого подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Вспомогательная функция для запуска миграций внутри асинхронного контекста."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме (с реальным подключением к БД)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())