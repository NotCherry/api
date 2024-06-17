from datetime import datetime
from typing import Union
from sqlmodel import Field, SQLModel, UUID
import uuid

class RecordExtender():
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now(), sa_column_kwargs={"onupdate": lambda: datetime.now()})

class Diagram(SQLModel, RecordExtender, table=True):
    __tablename__ = "diagrams"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description:str = Field(index=True)
    owner_id: str = Field( ("users.id"))
    config: str = Field()

    owner_id: str = Field(foreign_key="user.id")

class User(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    password: str = Field()
    is_active: bool = Field(default=True)
    


class Organization(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    description: str = Field()
    owner_id: str = Field(foreign_key="user.id")

class UserOrganization(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # manager: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id")
    organization_id: str = Field(foreign_key="organization.id")

class Project(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    description: str = Field()
    owner_id: str = Field(foreign_key="user.id")
    organization_id: str = Field(foreign_key="organization.id")

class UserProject(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    manager: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id")
    project_id: str = Field(foreign_key="project.id")

class Token(SQLModel, RecordExtender, table=True ):
    id: int | None = Field(default=None, primary_key=True)
    access_token: str
    token_type: str


class TokenData(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: Union[str, None] = None


class TokenDataScopes(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token_data_id: str = Field(foreign_key="tokendata.id")
    scope: str = Field()




