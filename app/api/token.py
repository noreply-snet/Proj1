from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import user_sch
from app.db.session import get_db
from app.core import security
from app.core.security import jwt_manager
from app.crud.jwt_curd import cleanup_expired_tokens,get_expired_tokens

router = APIRouter()



@router.post("/token", response_model=user_sch.Token)
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




@router.post("/refresh-token", response_model=user_sch.Token)
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


@router.get("/cleanup-tokens")
def cleanup_token(db: Session = Depends(get_db)):
    cleanup_expired_tokens(db=db)  
    return {"message": "Expired tokens cleaned up successfully."}    

    # try:
    #     cleanup_expired_tokens(db=db)  
    #     return {"message": "Expired tokens cleaned up successfully."}
    # except Exception as e:
    #     # Log the exception if necessary
    #     raise HTTPException(status_code=500, detail=str(e))


@router.get("/exp-tokens")
def get_exp_token(db: Session = Depends(get_db)):
    try:
        return get_expired_tokens(db=db) 
    except Exception as e:
        # Log the exception if necessary
        raise HTTPException(status_code=500, detail=str(e))