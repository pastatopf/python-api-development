from typing_extensions import ParamSpecKwargs
from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.sqltypes import DateTime

from app.database import Base
from datetime import datetime

# refered as Schema/Pydantic Model - check a request from user against this model
# defines the structure of a request & response
# ensures that when a user wants to create a post, the request will only go though if it has certain fields in the body (here title and content)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str