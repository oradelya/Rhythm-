from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends  # Импортируем Depends из fastapi
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:12345@localhost:5433/dance_workshops_db"  # Путь к базе данных

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