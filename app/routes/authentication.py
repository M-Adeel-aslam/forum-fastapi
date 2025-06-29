from fastapi import APIRouter, Depends,HTTPException
import models, schema
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import create_access_token
from utils import hashed_password, verify_password
from database import get_db

route = APIRouter(
    prefix="/auth",
    tags=['auth']
)
@route.post("/register", response_model=schema.UserOut)
async def register(user:schema.Usercreate, db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email ==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="user email already exists!")
    encrpyted_password = hashed_password(user.password) 
    newUser =models.User(
        username=user.username,
        email = user.email,
        password = encrpyted_password
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@route.post("/login")
async def login(login_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == login_form.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(login_form.password, user.password): 
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token =create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
   

    

    