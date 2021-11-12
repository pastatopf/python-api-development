from .. import models, schemas, oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List

router = APIRouter(prefix="/posts", tags=["Posts"])

# this is how it is done with regular SQL
# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM posts ")
#     posts = cursor.fetchall()
#     return {"data": posts}

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional [str] = ""):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# just for testing purposes as first step, when working without databases
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post, response: Response):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(1,1000000)
#     my_posts.append(post_dict)
#     return {"data": post_dict}

# this is how it is done with regular SQL
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",(post.title, post.content, post.published))
#     # Never do this, this will support SQL Injection. The above statement sanitizes that
#     # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title},{post.content},{post.published})")
#     conn.commit()
#     new_post = cursor.fetchone()
#     return {"data": new_post}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # takes post and converts it to a dictionary and unpack it with **
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    # retrieve created post
    db.refresh(new_post)
    return new_post

# just for testing purposes as first step, when working without databases
# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     post = find_post(id)
#  #   print(post)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id: {id} was not found"}
#     return {"post_detail": post}

# this is how it is done with regular SQL
# @app.get("/posts/{id}")
# def get_post(id: int):
#     # cursor.execute("SELECT * FROM posts WHERE id = %s",(id))
#     cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id),))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id: {id} was not found"}
#     return {"post_detail": post}

@router.get("/{id}",  response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return post

# just for testing purposes as first step, when working without databases
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     # find the index in the array that has required ID
#     index = find_index_post(id)
#     # print(index)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# this is how it is done with regular SQL
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *",(str(id),))
#     # index = find_index_post(id)
#     conn.commit()
#     deleted_post = cursor.fetchone()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # define query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # get the post
    post = post_query.first()

    # Checks if the post which he wants to delete exists
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    # checks if user wants to delete his own post, only this is permited
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    # delete the post
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# just for testing purposes as first step, when working without databases
# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     print(post)
#     index = find_index_post(id)
#     # print(index)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return {'data': post_dict}

# this is how it is done with regular SQL
# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
#     conn.commit()
#     updated_post = cursor.fetchone()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
#     return {"data": updated_post}

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query to find post with specific id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # grab that specific post
    post = post_query.first()
    # if it doesn't exist run a 404
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    # if the post is not a post from the logged in user throw an error
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    # if it exists update it 
    post_query.update(updated_post.dict(), synchronize_session=False)
    # commit this changes
    db.commit()
    # return the post
    return post_query.first()
