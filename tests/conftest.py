from jose import jwt
import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.database import get_db, Base
from app.config import settings
from app.main import app
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    login_data={"email": "hello123@gmail.com","password": "pass123"}
    res = client.post("/users/", json=login_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = login_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    login_data={"email": "hello420@gmail.com","password": "pass123"}
    res = client.post("/users/", json=login_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = login_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={'user_id':test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client


@pytest.fixture
def sample_posts(session, test_user, test_user2):
    post_data_list = [
        {"title": f"Sample Test Post {i}", "content": f"Sample content for test post {i}.", "owner_id": test_user['id']}
        for i in range(3)  # Creates 3 sample posts
    ]
    post_data_list.append({"title": "Sample Test Post 4", "content": "Sample content for test post by user2", "owner_id": test_user2['id']})
    
    # Using map to create Post models and add them to the session
    posts = list(map(lambda data: models.Post(**data), post_data_list))
    session.add_all(posts)
    session.commit()
    
    return posts  # This will yield a list of Post objects


@pytest.fixture
def test_post(test_user):
    return  {
        "title": "Sample Test Post",
        "content": "Sample content for test post",
        "published" : True
    }