from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.DB import db,schemas
from app.Crud import user_crud
from app.Auth import security
from app.Auth.auth_crud import revoke_token
from typing import List,Optional,Union
from datetime import datetime

router = APIRouter()

@router.post("/",response_model=schemas.UserResponse)
def user_create(user_data:schemas.UserCreate,db:Session = Depends(db.get_db)):
    return user_crud.create_user(db=db,user=user_data)

@router.post("/logout")
def logout(token: str = Depends(security.oauth2_scheme), db: Session = Depends(db.get_db)):
    payload = security.verify_token(db=db, token=token)
    revoke_token(db=db, token_id=payload["jti"], expires_at=datetime.fromtimestamp(payload["exp"]))
    return {"message": "Logged out successfully"}




lockRoutes = APIRouter(
    dependencies=[Depends(security.get_current_user)]
)




@lockRoutes.get("/",response_model=List[schemas.UserResponse])
def read_user(db:Session = Depends(db.get_db)):
    return user_crud.get_users(db=db)

