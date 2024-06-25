from datetime import datetime
from typing import Union
from sqlmodel import Field, SQLModel


class RecordExtender():
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now(
    ), sa_column_kwargs={"onupdate": lambda: datetime.now()})


class Diagram(SQLModel, RecordExtender, table=True):
    __tablename__ = "diagrams"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(index=True)
    config: str = Field()
    project_id: str = Field(foreign_key="project.id")


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
    manager: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id")
    organization_id: str = Field(foreign_key="organization.id")


class Project(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    description: str = Field()
    owner_id: int = Field(foreign_key="user.id")
    status_code: int = Field(foreign_key="projectstatuscode.id")
    organization_id: int | None = Field(foreign_key="organization.id")


class ProjectStatusCode(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str = Field(default="In Progress")


class UserProject(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    manager: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id")
    project_id: str = Field(foreign_key="project.id")


class Token(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    access_token: str
    token_type: str


class TokenData(SQLModel, RecordExtender, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: Union[str, None] = None