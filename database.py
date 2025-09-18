import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine=create_engine(database_url)
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
Base= declarative_base()
