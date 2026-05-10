from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "dance_workshops_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


@router.post("/register-user", response_model=schemas.TokenResponse)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({
        "id": new_user.id,
        "role": "user",
        "email": new_user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "user",
        "id": new_user.id,
        "name": new_user.name
    }


@router.post("/register-teacher", response_model=schemas.TokenResponse)
def register_teacher(teacher: schemas.TeacherRegister, db: Session = Depends(get_db)):
    existing_teacher = db.query(models.Teacher).filter(models.Teacher.email == teacher.email).first()

    if existing_teacher:
        raise HTTPException(status_code=400, detail="Teacher with this email already exists")

    new_teacher = models.Teacher(
        name=teacher.name,
        email=teacher.email,
        style=teacher.style,
        experience=teacher.experience,
        password_hash=hash_password(teacher.password)
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    token = create_access_token({
        "id": new_teacher.id,
        "role": "teacher",
        "email": new_teacher.email
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "teacher",
        "id": new_teacher.id,
        "name": new_teacher.name
    }


@router.post("/login", response_model=schemas.TokenResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if user and verify_password(data.password, user.password_hash):
        token = create_access_token({
            "id": user.id,
            "role": "user",
            "email": user.email
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "user",
            "id": user.id,
            "name": user.name
        }

    teacher = db.query(models.Teacher).filter(models.Teacher.email == data.email).first()

    if teacher and verify_password(data.password, teacher.password_hash):
        token = create_access_token({
            "id": teacher.id,
            "role": "teacher",
            "email": teacher.email
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "teacher",
            "id": teacher.id,
            "name": teacher.name
        }

    raise HTTPException(status_code=401, detail="Invalid email or password")