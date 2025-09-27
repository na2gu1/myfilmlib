from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from typing import Optional

# Загружаем .env (на всякий случай, если ещё не загружен)
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")  # fallback для тестов
    TMDB_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"  # игнорировать лишние переменные

# Экземпляр настроек — используем его везде в проекте
settings = Settings()