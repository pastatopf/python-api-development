# for what?
from typing import Optional
# to import different fastapi modules
from fastapi import FastAPI,Response,status,HTTPException
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

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
my_posts = [{"title": "title of post 1", "content": "content of post 1","id": 1},
           {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    print(id)
    print(my_posts)
    for i,p in enumerate(my_posts):
        print (i,p)
        if p['id'] == id:
            print(i)
            return i

@app.get("/")
def root():
    return {"message": "Welcome to my super visual studio API"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts ")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, response: Response):
    # just for testing purposes as first step, when working without databases
    # post_dict = post.dict()
    # post_dict['id'] = randrange(1,1000000)
    # my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
 #   print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    # print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)
    # print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}
    