from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, FastAPI

from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.crud import get_current_user
from .routers import limiter

from src.routers import auth

from .routers import graph_processor
from .routers import user

from .database import engine

load_dotenv()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(graph_processor.router)
app.include_router(user.router)
app.include_router(auth.router)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def get(token: Annotated[str, Depends(get_current_user)]):
    return JSONResponse(content={"message": "Hello, World"}, status_code=200)
