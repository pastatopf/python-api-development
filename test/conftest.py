# every test will access to the fixtures definded here
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
import pytest
# if alembic should be used instead of sqlalchemy
from alembic import command


# Option 1 - hardcode db connection
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastapi_test'/
# Option 2 - with env variables + '_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# scope - when to run this fixture, e.g. function, module, package, class
# best practice unit test: Test should not depend on each other

@pytest.fixture(scope="function")
def session():
    print("my session fixture run")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# fixture to setup db structure and delete the content of our database before/after each test
@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # better to put this here 
    # Base.metadata.drop_all(bind=engine)
    # # run our code before we return our test
    # Base.metadata.create_all(bind=engine)
    # if alembic should be used, add this
    # command.upgrade("head")
    yield TestClient(app)
    # run our code after our test finishes
    # Base.metadata.drop_all(bind=engine)
    # command.downgrade("base")

@pytest.fixture
def test_user(client):
    user_data = {"email":"hihi@gmail.com","password": "abc123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    #print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"hihi123@gmail.com","password": "abc123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    #print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    # taking dictionary to convert it to the desired format
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    # one way to do it manually
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])

    session.commit()
    posts = session.query(models.Post).all()
    return posts