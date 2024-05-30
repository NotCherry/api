from sqlalchemy.orm import Session

from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_Diagrams(db: Session, user_id: str):
    return db.query(models.Diagram).filter(models.Diagram.owner_id == user_id).all()


def create_user_item(db: Session, item: schemas.DiagramCreate, user_id: int):
    db_diagram = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_diagram)
    db.commit()
    db.refresh(db_diagram)
    return db_diagram