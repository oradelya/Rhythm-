from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)

    orders = relationship("Order", back_populates="user")


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    style = Column(String)
    experience = Column(String)
    password_hash = Column(String)

    workshops = relationship("Workshop", back_populates="teacher")
    orders = relationship("Order", back_populates="teacher")


class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    style = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    description = Column(String)
    date = Column(String)
    time = Column(String)
    location = Column(String)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="workshops")

    orders = relationship("Order", back_populates="workshop")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)

    workshop_id = Column(Integer, ForeignKey("workshops.id"))
    status = Column(String)

    user = relationship("User", back_populates="orders")
    teacher = relationship("Teacher", back_populates="orders")
    workshop = relationship("Workshop", back_populates="orders")