from typing import Optional,Dict
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_verified: bool
    otp: str

class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str
   


class UserCreate(UserBase):
    password: str


class UserVerify(BaseModel):
    username: str
    otp: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str
    content: str

class NoteInDB(NoteCreate):
    id: int
    
class Note(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: str
    

