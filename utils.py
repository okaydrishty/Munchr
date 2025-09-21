from passlib.context import CryptContext
import random
from random import randint

pwd_context= CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_pass,hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)

def otp_genrator():
    otp=""
    for i in range(6):
        otp+=str(random.randint(0,9))
    return otp

def otp_verifier(otp:str,user_no:str):
    
    if otp==user_no:
        return True
    else:
        return False