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
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="User exists")
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}
