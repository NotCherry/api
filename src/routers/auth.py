from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from typing import Annotated
import os
from fastapi.security import OAuth2PasswordRequestForm

from src.auth_tools import authenticate_user, create_access_token
from src.models import Token


router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    t = Token(access_token=access_token, token_type="bearer")
    print(t)
    return t



