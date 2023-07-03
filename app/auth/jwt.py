# from datetime import datetime, timedelta
# from jose import JWTError, jwt

# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expires})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         return None

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer,HTTPBearer
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from typing import Optional

# from app.auth import schemas
# from app.database import models

# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# oauth2_scheme = HTTPBearer(tokenUrl="token")

# SECRET_KEY = "secretisnotsecretanymore"  
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> models.User:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail="Invalid authentication credentials",
#                                 headers={"WWW-Authenticate": "Bearer"})
#         token_data = schemas.TokenData(username=username)
#         user = get_user_by_username(token_data.username)
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail="Invalid authentication credentials",
#                                 headers={"WWW-Authenticate": "Bearer"})
#         return user
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Invalid authentication credentials",
#                             headers={"WWW-Authenticate": "Bearer"})

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user_by_username(username: str) -> Optional[models.User]:
#     for user in models.USERS:
#         if user.username == username:
#             return user
#     return None

# def authenticate_user(username: str, password: str) -> Optional[models.User]:
#     user = get_user_by_username(username)
#     if not user:
#         return None
#     if not verify_password(password, user.password):
#         return None
#     return user


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session


from app.auth import schemas
from app.database import models
from app.database.database import SessionLocal

oauth2_scheme = HTTPBearer()

SECRET_KEY = "secretisnotsecretanymore"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# async def get_current_active_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> models.User:
#     try:
#         token = credentials.credentials
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         token_data = schemas.TokenData(username=username)
#         user = get_user_by_username(token_data.username,db)
#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         return user
#     except (JWTError, ValueError):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),db: Session = Depends(get_db)) -> models.User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = get_user_by_username(username, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# def get_user_by_username(username: str) -> Optional[models.User]:
#     for user in models.USERS:
#         if user.username == username:
#             return user
#     return None

from sqlalchemy.orm import Session

def get_user_by_username(username: str, db: Session) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
