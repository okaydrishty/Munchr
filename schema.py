from database import Base, engine, Sessionlocal
from models import User, Post, Recipe
from sqlalchemy import Column, Integer,String, Boolean, TIMESTAMP,text
from sqlalchemy.sql.expression import null
from typing import Optional
from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    email:str
    password:str

class UserCreate(BaseModel):
    email:str
    password:str
    name:str

class UserOut(BaseModel):
    email:str
    class config:
        orm_mode=True

class PostCreate(BaseModel):
    title: str
    content: str
    image:str

class PostResponse(BaseModel):
    post_id:int
    title:str
    content:str
    image:str

    class Config:
        orm_mode = True 

class ReciCreate(BaseModel):
    title: str
    content: str
    image:str

class ReciResponse(BaseModel):
    reci_id:int
    title:str
    content:str
    image:str

    class Config:
        orm_mode = True 

class Token(BaseModel):
    access_token:str
    token_type: str
    
class Token_Data(BaseModel):
    id:Optional[str]=None