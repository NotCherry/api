from typing import Union

from pydantic import BaseModel


class DiagramBase(BaseModel):
    title: str
    description: Union[str, None] = None
    config: str


class DiagramCreate(DiagramBase):
    pass


class Diagram(DiagramBase):
    id: int
    owner_id: int
    config: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    diagrams: list[Diagram] = []

    class Config:
        from_attributes = True