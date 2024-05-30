from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routers import graph_processor
from .routers import user

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(graph_processor.router)
app.include_router(user.router)

@app.get("/")
async def get():
    return JSONResponse(content={"message": "Hello, World"}, status_code=200)


