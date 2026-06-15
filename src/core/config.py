from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Настройки базы данных
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Секретный ключ для JWT (пригодится на следующем этапе)
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    @property
    def DATABASE_URL(self) -> str:
        """Собирает строку подключения для SQLAlchemy."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Указываем, что настройки нужно читать из файла .env в корне проекта
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Создаем синглтон (один объект настроек на все приложение)
settings = Settings()