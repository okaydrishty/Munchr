from fastapi import FastAPI, Response, status , HTTPException, Depends, APIRouter
import models,utils,database,schema
from sqlalchemy.orm import Session
from database import get_db
from routers import oauth2


router=APIRouter(
    prefix="/users",
    tags=['users']
)

oauth2_scheme = oauth2.OAuth2PasswordBearer(tokenUrl="token")


@router.post("/createaccount",status_code=status.HTTP_201_CREATED, response_model=schema.UserOut )
def create_user(user:schema.UserCreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
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