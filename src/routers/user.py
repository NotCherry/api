from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from sqlmodel import SQLModel


from ..crud import get_current_active_user, get_current_user, get_user_email, get_user_username, get_users, create_user
from ..models import User

router = APIRouter()

@router.get("/user/{username}")
def user(username: str):
    return get_user_username(username)

@router.get("/users", response_model=list[User])
def users(token: Annotated[str, Depends(get_current_user)]):
    return get_users()

class CreateUser(SQLModel):
    email: str
    password: str

@router.post("/users")
def db_create_user(user: User):
    db_user = get_user_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = get_user_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(email=user.email, username=user.username, password=user.password)

@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

