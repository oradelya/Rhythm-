from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    if order.user_id is None and order.teacher_id is None:
        raise HTTPException(
            status_code=400,
            detail="User ID or Teacher ID is required"
        )

    if order.user_id is not None and order.teacher_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Choose only one: user_id or teacher_id"
        )

    if order.user_id is not None:
        user = db.query(models.User).filter(models.User.id == order.user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    if order.teacher_id is not None:
        teacher = db.query(models.Teacher).filter(models.Teacher.id == order.teacher_id).first()

        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")

    workshop = db.query(models.Workshop).filter(models.Workshop.id == order.workshop_id).first()

    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    new_order = models.Order(
        user_id=order.user_id,
        teacher_id=order.teacher_id,
        workshop_id=order.workshop_id,
        status="pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/orders", response_model=list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@router.put("/orders/{order_id}", response_model=schemas.OrderResponse)
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if status not in ["pending", "paid", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    order.status = status
    db.commit()
    db.refresh(order)

    return order


@router.get("/users/{user_id}/orders", response_model=list[schemas.OrderResponse])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()


@router.get("/teachers/{teacher_id}/orders", response_model=list[schemas.OrderResponse])
def get_teacher_orders(teacher_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.teacher_id == teacher_id).all()


@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted"}