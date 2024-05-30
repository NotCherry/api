from sqlmodel import Session, select

from . import models


def create_user(db: Session, user: models.User):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_item(db: Session, item: models.Diagram, user_id: int):
    db_diagram = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_diagram)
    db.commit()
    db.refresh(db_diagram)
    return db_diagram