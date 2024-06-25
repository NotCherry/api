from fastapi.testclient import TestClient

from sqlmodel import SQLModel, Session, create_engine

from src.tests.initialize_data import init_status_code

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

TEST_PROJECT = {"owner_id": 1, "name": "Test Project", "description": "This is a test project", "organization_id": None, "status_code": 1}



def create_user():
    response = client.post(
        "/users/",
        json=TEST_USER,
    )
    assert response.status_code == 200, response.text

    return response.json()

def get_token():
    response = client.post(
        "/token",
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]},
    )
    assert response.status_code == 200, response.text

    return response.json()["access_token"]

def auth_header():
    return {"Authorization": f"Bearer {get_token()}"}

def test_create_user():
    init_db()

    data = create_user()

    assert "id" in data
    assert data["email"] == TEST_USER["email"]
    assert data["username"] == TEST_USER["username"]
    assert data["password"] is None


def test_get_user_by_id():
    init_db()
    user_id = create_user()["id"]
    

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == TEST_USER["email"]
    assert data["username"] == TEST_USER["username"]

    
def test_create_user_project():
    init_db()
    user_id = create_user()["id"]

    init_status_code(Session(engine))

    response = client.post(
        "/projects",
        json=TEST_PROJECT,
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert data["name"] == TEST_PROJECT["name"]
    assert data["description"] == TEST_PROJECT["description"]
    assert int(data["owner_id"]) == user_id
    assert data["status_code"] == 1


def test_get_user_projects():
    init_db()
    user_id = create_user()["id"]
    init_status_code(Session(engine))
    response = client.post(
        "/projects",
        json=TEST_PROJECT,
        headers=auth_header()
    )
    assert response.status_code == 200, response.text
   
    response = client.get(f"/projects", headers=auth_header())

    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == TEST_PROJECT["name"]
    assert data[0]["description"] == TEST_PROJECT["description"]
    assert int(data[0]["owner_id"]) == user_id
    assert data[0]["status_code"] == 1

def test_create_org():
    pass

def test_create_org_project():
    pass

def test_get_org_projects():
    pass