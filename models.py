from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from database import Base 
from sqlalchemy.orm import relationship
from typing import Optional


class User(Base): 
    __tablename__="user"
    email=Column(String,unique=True,index=True,nullable= False)
    hashed_password=Column(String)
    name=Column(String,nullable=False)
    userid=Column(Integer, nullable=False, primary_key=True, index=True)
    created_at=Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(),nullable=True)
    recipes = relationship("Recipe", back_populates="author")
    posts = relationship("Post", back_populates="author")



class Recipe(Base):
    __tablename__="recipes"
    reci_id=Column(Integer, nullable=False, primary_key=True, index=True)
    title=Column(String,index=True,nullable=True)
    content=Column(String,index= True,nullable=False)
    authorid=Column(Integer, ForeignKey('user.userid'),nullable=False,index=True)
    image_url = Column(String, nullable=True)
    created_at=Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(),nullable=True)
    author = relationship("User", back_populates="recipes")


class Post(Base):
    __tablename__="posts"
    post_id=Column(Integer, nullable=False, primary_key=True, index=True)
    title=Column(String,index=True)
    content=Column(String,index= True,nullable=False)
    authorid=Column(Integer,ForeignKey('user.userid'), nullable=False,index=True)
    image_url = Column(String, nullable=True)
    created_at=Column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(),nullable=True)
    author = relationship("User", back_populates="posts")

class Recilike(Base):
    __tablename__ = "recilikes" 
    userid=Column(Integer,ForeignKey('user.userid'),primary_key=True)
    reci_id=Column(Integer,ForeignKey('recipes.reci_id'),primary_key=True)

class Postlike(Base):
    __tablename__ = "postlikes" 
    userid = Column(Integer, ForeignKey("user.userid"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), primary_key=True)

class Postdislikes(Base):
    __tablename__ = "postdislikes"

    userid = Column(Integer,
                    ForeignKey("user.userid"),
                    primary_key=True)
    post_id = Column(Integer,
                     ForeignKey("posts.post_id"),
                     primary_key=True)