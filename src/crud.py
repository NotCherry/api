import os
from typing import Annotated
from fastapi import Depends, HTTPException
import jwt

from sqlmodel import Session, select

from src.util import get_password_hash
from . import models
from .util import get_db, oauth2_scheme
from .exceptions import credentials_exception


def create_user(db: Session, email: str, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = models.User(email=email, username=username,
                          password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_project(db: Session, project: models.Project):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def create_diagram_in_project(db: Session, diagram: models.Diagram, project_id: int):
    db_diagram = models.Item(**diagram.model_dump(), owner_id=project_id)
    db.add(db_diagram)
    db.commit()
    db.refresh(db_diagram)
    return db_diagram


def get_projects_by_user(db: Session, id: int):
    return db.exec(select(models.Project).where(models.Project.owner_id == id)).all()

def get_users(db: Session):
    return db.exec(select(models.User)).all()


def get_user_id(db: Session, id: int):
    return db.exec(select(models.User).where(models.User.id == id)).first()


def get_user_email(db: Session, email: str):
    return db.exec(select(models.User).where(models.User.email == email)).first()


def get_user_username(db: Session, username: str):
    return db.exec(select(models.User).where(models.User.username == username)).first()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> models.User:
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"),
                             algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)

    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")

    user = {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
    }
    return user


def get_projects_by_org(db: Session, org_id: str):
    return db.exec(select(models.Project).where(models.Project.organization_id == org_id)).all()


def get_org_by_user(db: Session, user_id: str)-> models.UserOrganization:
    return db.exec(select(models.UserOrganization).where(models.UserOrganization.user_id == user_id)).first()