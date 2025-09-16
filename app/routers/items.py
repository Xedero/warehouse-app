from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@router.post("/")
def create_item(name: str, quantity: int = 0, sku: str = None, db: Session = Depends(get_db)):
    if db.query(models.Item).filter(models.Item.name == name).first():
        raise HTTPException(status_code=400, detail="Item exists")
    item = models.Item(name=name, quantity=quantity, sku=sku)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
