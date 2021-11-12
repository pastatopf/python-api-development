# to import different fastapi modules
from fastapi import FastAPI, security
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my super visual studio API"}

# just for testing, store data in memory instead of database as a first step
# my_posts = [{"title": "title of post 1", "content": "content of post 1","id": 1},
#            {"title": "favorite foods", "content": "I like pizza", "id": 2}]
#
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
#
# def find_index_post(id):
#     print(id)
#     print(my_posts)
#     for i,p in enumerate(my_posts):
#         print (i,p)
#         if p['id'] == id:
#             print(i)
#             return i

