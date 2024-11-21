from dataclasses import dataclass
from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.crud import get_current_user, get_diagram_by_id, update_diagram_config
from src.models import User
from src.util import get_db
from pydantic import BaseModel

router = APIRouter()

class Data(BaseModel):
    id: str
    config: str

@router.put("/diagram")
def update_diagrams(data: Data, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return update_diagram_config(db, data.id, data.config,  user.id)

@router.get("/diagram/{diagram_id}")
def diagrams(diagram_id:int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_diagram_by_id(db, diagram_id, user.id)
