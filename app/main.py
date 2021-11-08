# for runtime support for type hints
from typing import Optional
# to import different fastapi modules
from fastapi import FastAPI,Response,status,HTTPException,Depends
# to import http bodies
from fastapi.params import Body
# to create a defined BaseModel
from pydantic import BaseModel
# to generate random numbers
from random import randrange
# for postgres driver
import psycopg2
# for cursor_factory=RealDictCursor
from psycopg2.extras import RealDictCursor
# for sleep command
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',
        password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my super visual studio API"}