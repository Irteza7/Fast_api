from http import client
import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app import schemas

# @pytest.mark.parametrize() # pass in multiple parameter sets to test diff input args
# @pytest.fixture # function that runs before a specific test case
# with pytest.raises(Exception) # to check if test fails if expected to fail

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# client = TestClient(app)

@pytest.fixture
def client():
    # run code before we run our test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # run code after running the test
    

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message')== 'Hello World!!!'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "irteza@gmail.com",
                                       "password": "pass123"})
    new_user = schemas.UserOut(**res.json())
    # print(res.json())
    assert new_user.email == "irteza@gmail.com"
    assert res.status_code == 201