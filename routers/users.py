from fastapi import FastAPI, Response, status , HTTPException, Depends, APIRouter
import models,utils,database,schema,email
from sqlalchemy.orm import Session
from database import get_db
from routers import oauth2
import cachetools 
from cachetools import TTLCache
import random
from random import randint
import smtplib 
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

pending_users = TTLCache(maxsize=1000, ttl=300)



router=APIRouter(
    prefix="/users",
    tags=['users']
)

oauth2_scheme = oauth2.OAuth2PasswordBearer(tokenUrl="token")


@router.post("/createaccount",status_code=status.HTTP_201_CREATED, response_model=schema.UserOut )
def create_user(user:schema.UserCreate,db:Session=Depends(get_db)):
    
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    to_mail= user.email

    pending_users[user.email] = {
        "otp": otp,
        "hashed_password": hashed_password,
        "name": user.name
    }

   

    otp= utils.otp_genrator()

    msg=EmailMessage()
    msg['Subject']="OTP Verification"
    msg['From']=email.sender_mail
    msg['To']=user.email
    msg.set_content(f"Your otp is{otp}")
    
    #email sending
    try:
        email.send_email(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to send verification email, try a valid account")
    
    return{"message":"OTP sent successfully"}

@router.post("/createaccount/verify otp")
def verifying(email:str,otp:str,db:Session=Depends(get_db)):
    cached = pending_users.get(email)
    if not cached:
        raise HTTPException(status_code=400,detail="otp expired or user not found")
    
    if cached["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    new_user = models.User(
        email=cached[email],
        name=cached["name"],
        hashed_password=cached["hash_password"])
    

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    del pending_users[email]
    
    return new_user

@router.delete("/deleteaccount")
def delete_user():
    pass

@router.put("/changepassword")
def changepassword():
    pass

@router.put("/changename")
def changename():
    pass

@router.get("/{userid}", response_model=schema.UserOut)
def get_user(userid: int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.userid==userid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with {userid} doesnot exists")
    return user