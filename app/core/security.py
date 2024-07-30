# auth.py
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.services.hashing import verify_password
from app.services.jwt import get_user_by_paload,verify_token
from app import crud
from app.db.session import get_db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")



def authenticate_user(db: Session, username: str, password: str):
    user = crud.user.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    payload = verify_token(db=db, token=token)
    return get_user_by_paload(
        db=db,
        payload=payload
    )
