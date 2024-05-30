from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..database import engine
from .. import crud, models

router = APIRouter()

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=list[models.User])
def users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

@router.get("/user/{user_id}")
def user():
    return crud.get_user()


@router.post("/users/", response_model=models.User)
def create_user(user: models.User):
    with Session(engine) as db:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db=db, user=user)
