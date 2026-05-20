import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Берем DATABASE_URL из Render/Neon
# Если её нет — используем локальную PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:12345@localhost:5433/dance_workshops_db"
)

# Подключение к базе данных
engine = create_engine(DATABASE_URL)

# Создание сессии
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Базовый класс моделей
Base = declarative_base()