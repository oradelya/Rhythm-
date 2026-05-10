from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/workshops", response_model=schemas.WorkshopResponse)
def create_workshop(
    workshop: schemas.WorkshopCreate,
    db: Session = Depends(get_db)
):
    if workshop.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    teacher = db.query(models.Teacher).filter(models.Teacher.id == workshop.teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    new_workshop = models.Workshop(
        title=workshop.title,
        style=workshop.style,
        price=workshop.price,
        image_url=workshop.image_url,
        teacher_id=workshop.teacher_id,
        description=workshop.description,
        date=workshop.date,
        time=workshop.time,
        location=workshop.location,
    )

    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)

    return new_workshop


@router.get("/workshops", response_model=list[schemas.WorkshopResponse])
def get_workshops(db: Session = Depends(get_db)):
    return db.query(models.Workshop).all()


@router.get("/workshops/style/{style}", response_model=list[schemas.WorkshopResponse])
def get_by_style(style: str, db: Session = Depends(get_db)):
    return db.query(models.Workshop).filter(models.Workshop.style == style).all()


@router.delete("/workshops/{workshop_id}")
def delete_workshop(workshop_id: int, db: Session = Depends(get_db)):
    workshop = db.query(models.Workshop).filter(models.Workshop.id == workshop_id).first()

    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    db.delete(workshop)
    db.commit()

    return {"message": "Workshop deleted"}

@router.get("/teachers/{teacher_id}/workshops", response_model=list[schemas.WorkshopResponse])
def get_teacher_workshops(teacher_id: int, db: Session = Depends(get_db)):
    return db.query(models.Workshop).filter(models.Workshop.teacher_id == teacher_id).all()

@router.put("/workshops/{workshop_id}", response_model=schemas.WorkshopResponse)
def update_workshop(
    workshop_id: int,
    workshop_data: schemas.WorkshopCreate,
    db: Session = Depends(get_db)
):
    workshop = db.query(models.Workshop).filter(models.Workshop.id == workshop_id).first()

    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    workshop.title = workshop_data.title
    workshop.style = workshop_data.style
    workshop.price = workshop_data.price
    workshop.image_url = workshop_data.image_url
    workshop.description = workshop_data.description
    workshop.date = workshop_data.date
    workshop.time = workshop_data.time
    workshop.location = workshop_data.location
    workshop.teacher_id = workshop_data.teacher_id

    db.commit()
    db.refresh(workshop)

    return workshop