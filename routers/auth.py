from fastapi import APIRouter, Depends, status,HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import database, models, utils
from . import oauth2

router=APIRouter(tags=["Authentication"])

@router.post('/login')
def login (user_credentials:OAuth2PasswordRequestForm =Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")
    #create token n return it
    access_token= oauth2.create_access_token(data={"user_id":user.userid})
    return {"accesstoken":access_token,"tokentype":"bearer"}