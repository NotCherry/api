from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from .routers import graph_processor
from .routers import user

from . import models
from .database import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)    

app.include_router(graph_processor.router)
app.include_router(user.router)

@app.get("/")
async def get():
    return JSONResponse(content={"message": "Hello, World"}, status_code=200)


