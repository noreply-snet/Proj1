from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import uuid

from app.schemas import schemas
from app.db.session import get_db
from app.core import security



router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    jwt_id = str(uuid.uuid4())
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires,jwi=jwt_id
    )
    refresh_token_expires = timedelta(minutes=security.REFRESH_TOKEN_EXPIRE_MINUTES,)
    refresh_token = security.create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires,jwi=jwt_id
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}




@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_access_token(db: Session = Depends(get_db), refresh_token: str  = ""):
    payload = security.verify_token(db=db, token=refresh_token)
    user = security.get_user_by_paload(db=db, payload=payload)

    jwt_id = str(uuid.uuid4())
    new_access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=new_access_token_expires,jwi=jwt_id
    )
    new_refresh_token_expires = timedelta(minutes=security.REFRESH_TOKEN_EXPIRE_MINUTES)
    new_refresh_token = security.create_refresh_token(
        data={"sub": user.username}, expires_delta=new_refresh_token_expires,jwi=jwt_id
    )
    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

