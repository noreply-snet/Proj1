from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta


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
    access_token, refresh_token = security.jwt_manager.generate_tokens(user.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}




@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_access_token(db: Session = Depends(get_db), refresh_token: str  = ""):
    payload = security.jwt_manager.verify_token(db=db, token=refresh_token)
    user = security.jwt_manager.get_user_by_paload(db=db, payload=payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    new_access_token, new_refresh_token = jwt_manager.generate_tokens(user.username)

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

