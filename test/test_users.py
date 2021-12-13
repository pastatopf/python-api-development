from app import schemas
import pytest
from jose import jwt
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Welcome to my super visual studio API!!!Hurrafadfad'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/",json={"email":"hihi@gmail.com", "password":"abc123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hihi@gmail.com"
    # assert res.json().get("email") == "halli@gmail.com"
    # assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login",data={"username":test_user['email'], "password":test_user['password']})
    # print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com','abc123', 403),
    ('hihi@gmail.com','wrongPassword', 403),
    ('wrongemail@gmail.com','wrongPassword', 403),
    (None,'abc123', 422),
    ('hihi@gmail.com','abc1234', 403),
    ('hihi@gmail.com',None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'