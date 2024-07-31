# auth.py
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.services.hashing import verify_password
from app.services.jwt import JWTManager
from app import crud
from app.db.session import get_db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

jwt_manager = JWTManager()  # Create an instance of JWTManager

def authenticate_user(db: Session, username: str, password: str):
    user = crud.user.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    payload = jwt_manager.verify_token(db=db, token=token)
    return jwt_manager.get_user_from_payload(
        db=db,
        payload=payload
    )
