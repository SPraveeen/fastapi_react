from fastapi.testclient import TestClient
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Task
import models

SQLALCHEMY_DATABASE_URL='sqlite:///./task_test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)


@pytest.fixture
def session():
    print("Creating fresh test database")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
        
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)

    
@pytest.fixture
def test_tasks(session):
    tasks_data=[
        {"taskname":"first task","description":"first description","status":"first status"},
        {"taskname":"second task","description":"second description","status":"second status"},
        {"taskname":"third task","description":"third description","status":"third status"},
        {"taskname":"fourth task","description":"fourth description","status":"fourth status"}
    ]

    def create_task_model(task):
        return models.Task(**task)
    task_map=map(create_task_model,tasks_data)
    tasks=list(task_map)

    session.add_all(tasks)
    session.commit()
    tasks=session.query(models.Task).all()
    return tasks

# @pytest.fixture
# def test_user2(client):
#     user_data={
#         "email":"hello1234@gmail.com",
#         "password":"123456"
#     }
#     res=client.post("/users/",json=user_data)
#     assert res.status_code==201
#     new_user=res.json()
#     new_user['password']=user_data['password']
#     return new_user

# @pytest.fixture
# def test_user(client):
#     user_data={
#         "email":"hello123@gmail.com",
#         "password":"123456"
#     }
#     res=client.post("/users/",json=user_data)
#     assert res.status_code==201
#     new_user=res.json()
#     new_user['password']=user_data['password']
#     return new_user

# @pytest.fixture
# def token(test_user):
#     return create_access_token({"user_id":test_user['id']})


# @pytest.fixture
# def authorized_client(client,token):
#     client.headers={
#         **client.headers,
#         "Authorization":f"Bearer {token}"
#     }
#     return client

# @pytest.fixture
# def test_posts(test_user,session,test_user2):
#     posts_data=[
#         {"title":"first title","content":"first content","owner_id":test_user['id']},
#         {"title":"second title","content":"second content","owner_id":test_user['id']},
#         {"title":"third title","content":"third content","owner_id":test_user['id']},
#         {"title":"fourth title","content":"fourth content","owner_id":test_user2['id']}
#     ]

#     def create_post_model(post):
#         return models.Post(**post)
#     post_map=map(create_post_model,posts_data)
#     posts=list(post_map)

#     session.add_all(posts)
#     # session.add_all([models.Post(title="first title",content="first content",owner_id=test_user['id']),
#     # models.Post(title="second title",content="second content",owner_id=test_user['id']),
#     # models.Post(title="third title",content="third content",owner_id=test_user['id'])])
#     session.commit()
#     posts=session.query(models.Post).all()
#     return posts

