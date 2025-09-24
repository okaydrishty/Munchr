from jose import JWTError, jwt
from datetime import datetime, timedelta
import models, database, schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme= OAuth2PasswordBearer(tokenUrl='/login')

access_token_time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
secret_key=os.getenv("SECRET_KEY")
algorithm=os.getenv("ALGORITHM")


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=access_token_time)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return encoded_jwt

def verify_access_token (token:str,credentials_exception):
    try:
        payload=jwt.decode(token,secret_key,algorithms=algorithm)
        id:str=payload.get("userid")
        if id is None:
            raise credentials_exception
        token_data=schema.Token_Data(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user (token:str=Depends (oauth2_scheme), db: Session =Depends(database.get_db)):
    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"couldnt validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token, credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()

    return verify_access_token(token,credentials_exception)