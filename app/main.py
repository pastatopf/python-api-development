# to import different fastapi modules
from fastapi import FastAPI, security
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# create tables definde in models, not needed with alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# domains, which can access our API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Succesfully Herokued with error"}

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
