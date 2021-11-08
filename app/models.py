from typing import Text
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from sqlalchemy.sql.expression import text
from .database import Base

# sqlalchemy model - responsible for defining the columns of our posts table with postgres - It is used to query, create, delete and update entries within the database
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
