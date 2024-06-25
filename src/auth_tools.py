from datetime import datetime, timedelta, timezone
from typing import  Union

from fastapi import Depends
from sqlmodel import Session

from src.util import get_db, verify_password
from .crud import get_user_email, get_user_username

import jwt
import os

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str ):
    user = get_user_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user