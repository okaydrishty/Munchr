from typing import Union
from fastapi import FastAPI
from database import Base, engine
from models import *  
from routers import users


app=FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users.router)