from sqlmodel import Field, SQLModel, UUID
import uuid

class Diagram(SQLModel, table=True):
    __tablename__ = "diagrams"

    id: str = Field(default=uuid.uuid4().__str__(), primary_key=True)
    title: str = Field(index=True)
    description:str = Field(index=True)
    owner_id: str = Field( ("users.id"))
    config: str = Field()

    owner_id: str = Field(foreign_key="user.id")

class User(SQLModel, table=True):
    id: str = Field(default=uuid.uuid4().__str__(), primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str = Field()
    is_active: bool = Field(default=True)

    # diagrams: list[Diagram] = Field(default=[])


