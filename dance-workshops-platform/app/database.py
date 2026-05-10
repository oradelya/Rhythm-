from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends  # Импортируем Depends из fastapi
from sqlalchemy.ext.declarative import declarative_base

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:12345@localhost:5433/dance_workshops_db"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
# Создаём объект Base
Base = declarative_base()

# Создаём подключение к базе данных
engine = create_engine(DATABASE_URL)

# Создаём сессию для взаимодействия с базой
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии базы данных
def get_db(db: Session = Depends(SessionLocal)):
    try:
        yield db
    finally:
        db.close()  # Закрывает сессию после выполнения запроса