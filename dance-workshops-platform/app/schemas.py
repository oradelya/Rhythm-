from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class TeacherCreate(BaseModel):
    name: str
    email: str
    style: str
    experience: str


class TeacherResponse(BaseModel):
    id: int
    name: str
    email: str
    style: str
    experience: str

    class Config:
        from_attributes = True


class WorkshopCreate(BaseModel):
    title: str
    style: str
    price: int
    teacher_id: int
    image_url: str
    description: str | None = None
    date: str | None = None
    time: str | None = None
    location: str | None = None


class WorkshopResponse(BaseModel):
    id: int
    title: str
    style: str
    price: int
    teacher_id: int
    teacher: TeacherResponse
    image_url: str
    description: str | None = None
    date: str | None = None
    time: str | None = None
    location: str | None = None
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    user_id: Optional[int] = None
    teacher_id: Optional[int] = None
    workshop_id: int


class OrderResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    teacher_id: Optional[int] = None
    workshop_id: int
    status: str

class Config:
    from_attributes = True
        
class UserRegister(BaseModel):
    name: str
    email: str
    password: str


class TeacherRegister(BaseModel):
    name: str
    email: str
    password: str
    style: str
    experience: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    id: int
    name: str