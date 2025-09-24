from fastapi import FastAPI, Response, status , HTTPException, Depends, APIRouter
import models,utils,database,schema,sendmail
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


@router.post("/createaccount",status_code=status.HTTP_201_CREATED )
def create_user(user:schema.UserCreate,db:Session=Depends(get_db)):
    
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    to_mail= user.email

    otp_og = utils.otp_genrator()

    pending_users[user.email] = {
        
        "hashed_password": hashed_password,
        "name": user.name,
        "otp":otp_og
    }



    msg=EmailMessage()
    msg['Subject']="OTP Verification"
    msg['From']=sendmail.sender_mail
    msg['To']=to_mail
    msg.set_content(f"Your otp is{otp_og}")
    
    #email sending
    try:
        sendmail.send_email(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to send verification email, try a valid account")
    
    return{"message":"OTP sent successfully"}



@router.post("/createaccount/verifyotp",status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def verifying(data:schema.OTPVerify,db:Session=Depends(get_db)):
    cached=pending_users.get(data.email)
    if not cached:
        raise HTTPException(status_code=400,detail="otp expired or user not found")
    
    if cached["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    new_user = models.User(
        email=data.email,
        name=cached["name"],
        hashed_password=cached["hashed_password"])
    

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    del pending_users[data.email]

    return new_user



@router.delete("/deleteaccount")
def delete_user(password:schema.Confirmpass,db:Session= Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    plain_password=password.password
    if not utils.verify(plain_password, current_user.hashed_password):
        raise HTTPException(status_code=403, detail="Incorrect password")

    db.delete(current_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    

@router.put("/changepassword")
def changepassword(password:schema.Changepass,db:Session= Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    old_password=password.old_password

    if not utils.verify(old_password, current_user.hashed_password):
        raise HTTPException(status_code=403, detail="Incorrect password")
    
    new_hashed_password=utils.hash(password.new_password)
    current_user.hashed_password=new_hashed_password
    db.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.get("/{userid}", response_model=schema.UserOut)
def get_user(userid: int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.userid==userid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with {userid} doesnot exists")
    return user