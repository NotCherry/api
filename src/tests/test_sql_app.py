from fastapi.testclient import TestClient

from sqlmodel import SQLModel, Session, create_engine

from ..main import app
from ..util import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def init_db():
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = Session(engine)
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

TEST_USER = {"email": "deadpool@example.com",
             "password": "chimichangas4life",
             "username": "testerjordan"}


def test_create_user():
    init_db()

    response = client.post(
        "/users/",
        json=TEST_USER,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    print(data, user_id)
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id


def test_get_user_by_username():
    init_db()
