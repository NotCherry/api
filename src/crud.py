import os
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
import jwt

from sqlmodel import Session, select

from .database import engine
from src.util import get_password_hash
from . import models
from .util import oauth2_scheme
from .exceptions import credentials_exception


def create_user(email: str, username: str, password: str):
    with Session(engine) as db:
        print(password)
        hashed_password = get_password_hash(password)
        print(hashed_password)
        db_user = models.User(email=email, username=username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


def create_user_diagram(diagram: models.Diagram, user_id: int):
    with Session(engine) as db:
        db_diagram = models.Item(**diagram.model_dump(), owner_id=user_id)
        db.add(db_diagram)
        db.commit()
        db.refresh(db_diagram)
        return db_diagram

def get_users():
    with Session(engine) as db:
        return db.exec(select(models.User)).all()

def get_user_email(email: str):
    with Session(engine) as db:
        return db.exec(select(models.User).where(models.User.email == email)).first()
    
def get_user_username(username: str):
    with Session(engine) as db:
        return db.exec(select(models.User).where(models.User.username == username)).first()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        print("validating!!")
        print(token)
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
        
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user_username(username=token_data.username)
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

async def get_projectsby_org(db: Session, org_id: str ):
    db.exec
    return db.exec(select(models.Project).where(models.Project.organization_id == org_id)).all()

