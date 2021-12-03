from app import schemas
from .database import client,session

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to my super visual studio API!!!Hurrafadfad'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/",json={"email":"hihi@gmail.com", "password":"abc123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hihi@gmail.com"
    # assert res.json().get("email") == "halli@gmail.com"
    # assert res.status_code == 201