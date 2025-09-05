from sqlalchemy.orm import Session
import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    obj = models.User(email=user.email, name=user.name)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def list_users(db: Session):
    return db.query(models.User).all()