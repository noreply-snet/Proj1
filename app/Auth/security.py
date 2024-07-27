# auth.py
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.Crud import user_crud
from app.DB import schemas,db


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = user_crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    u_name = ''
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # Check for time expiration 
        if "exp" in payload:
            if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        u_name=username
    except JWTError:
        raise credentials_exception
    
    return u_name


async def get_current_user(db:Session = Depends(db.get_db), token: str = Depends(oauth2_scheme)):
    username = verify_token(token=token)
    user = user_crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
