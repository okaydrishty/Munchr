from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base 
from sqlalchemy.orm import relationship
from typing import Optional

class User(Base): 
    __tablename__="user"
    email=Column(String,unique=True,index=True,nullable= False)
    hashed_password=Column(String)
    name=Column(String,nullable=False)
    userid=Column(Integer, nullable=False, primary_key=True, index=True)

    recipes = relationship("Recipe", back_populates="author")
    posts = relationship("Post", back_populates="author")



class Recipe(Base):
    __tablename__="recipes"
    reci_id=Column(Integer, nullable=False, primary_key=True, index=True)
    title=Column(String,index=True),Optional
    content=Column(String,index= True,nullable=False)
    authorid=Column(Integer, ForeignKey('user.userid'),nullable=False,index=True)

    author = relationship("User", back_populates="recipes")


class Post(Base):
    __tablename__="posts"
    post_id=Column(Integer, nullable=False, primary_key=True, index=True)
    title=Column(String,index=True)
    content=Column(String,index= True,nullable=False)
    authorid=Column(Integer,ForeignKey('user.userid'), nullable=False,index=True)
    
    author = relationship("User", back_populates="posts")