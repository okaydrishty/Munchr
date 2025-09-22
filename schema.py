from database import Base, engine, SessionLocal
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
    email:EmailStr
    password:str
    name:str

class UserOut(BaseModel):
    email:EmailStr
    class config:
        orm_mode=True

class Confirmpass(BaseModel):
    password:str

class Changepass(BaseModel):
    old_password:str
    new_password:str

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

class OTPVerify(BaseModel):
    email:str
    otp: str