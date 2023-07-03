from fastapi import APIRouter, Depends, HTTPException,Response,Request,Cookie
from sqlalchemy.orm import Session
from typing import List
import random
# from app.database.database import get_db
from app.database.models import User, Note
from app.auth import email, hash, jwt, schemas
from fastapi.responses import RedirectResponse


router = APIRouter()



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists.")

    # Hash password
    hashed_password = hash.get_password_hash(user.password)

    # Create user
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate and send OTP
    # otp="1234"
    otp = str(random.randint(1000, 9999))
    print("***-",otp)
    # response=RedirectResponse(url="/verify")
    # response.set_cookie(key="otp", value=otp)
    email.send_verification_email(user.username, user.email, otp)
    # print(otp_res,"new cookie")
    return new_user



@router.post("/verify", response_model=schemas.Token)
def verify_user(verification: schemas.UserVerify,otp:str ,db: Session = Depends(get_db)):
    # Retrieve user
    user = db.query(User).filter(User.username == verification.username).first()
    print("username>>",user.username)
    try:
        if not user:
            raise HTTPException(status_code=400, detail="User not found.")
        if user.is_verified:
            raise HTTPException(status_code=400, detail="User is already verified.")
    except Exception as ex:
        print("user nhi mil rha",ex)

#     # # Verify OTP
#     # request=Request()
#     # print("user=",user)
#     # print(verification.otp)
#     print("******************************")
#     print(otp)
    
    if user: 
        print("user mil rha")   
        if verification.otp != otp: #error here how to get otp from another function
            raise HTTPException(status_code=400, detail="Invalid OTP.")
    else:
        print("USER NAHI MIL RHA")
    user.is_verified = True
    print(user.username)
    db.commit()

    # Create JWT token
    access_token = jwt.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
def login_user(login: schemas.UserLogin, db: Session = Depends(get_db)):
    # Retrieve user
    user = db.query(User).filter(User.username == login.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="User is not verified.")

    # Verify password
    if not hash.verify_password(login.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password.")
    print("---->",user.username)

    # # Create JWT token
    # access_token = jwt.create_access_token({"sub": user.username})
    # return {"access_token": access_token, "token_type": "bearer"}


@router.post("/note", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(jwt.get_current_active_user)):
    new_note = Note(
        title=note.title,
        content=note.content,
        user_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


# @router.get("/note", response_model=List[schemas.Note])
# def get_user_notes(db: Session = Depends(get_db), current_user: User = Depends(jwt.get_current_active_user)):
#     notes = db.query(Note).filter(Note.user_id == current_user.id).all()
#     return notes
# from typing import List

@router.get("/note", response_model=List[schemas.Note])
def get_user_notes(db: Session = Depends(get_db), current_user: User = Depends(jwt.get_current_active_user)):
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    return [schemas.Note.from_orm(note) for note in notes]
