from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users import router as user_router
from app.workshops import router as workshop_router
from app.orders import router as order_router
from app.teachers import router as teacher_router
from app.database import engine
from app import models
from app.auth import router as auth_router

# Создаём FastAPI приложение
app = FastAPI(title="Dance Workshops Platform API")

# Создаём все таблицы
models.Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(user_router)
app.include_router(workshop_router)
app.include_router(order_router)
app.include_router(teacher_router)   
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Dance Workshops Platform API is running"}