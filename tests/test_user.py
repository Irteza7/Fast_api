import pytest 
from app import schemas
from app.config import settings
from jose import jwt

# @pytest.mark.parametrize() # pass in multiple parameter sets to test diff input args
# @pytest.fixture # function that runs before a specific test case
# with pytest.raises(Exception) # to check if test fails if expected to fail


# def test_root(client):
#     res = client.get("/")
#     # print(res.json().get('message'))
#     assert res.json().get('message')== 'Hello World!!!'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com",
                                       "password": "pass123"})
    new_user = schemas.UserOut(**res.json())
    # print(res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    # print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert res.status_code == 200


@pytest.mark.parametrize("username, password, status_code",
                        [("wrongemail@gmail.com", "pass123", 403),
                        ("hello123@gmail.com", "WrongPassword", 403),
                        (None, "pass123", 422),
                        ("123@gmail.com", None, 422)])
def test_incorrect_login(test_user, client, username, password, status_code):
    res = client.post("/login", data={"username": username, "password": password})

    assert res.status_code == status_code   
