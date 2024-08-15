from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from datetime import datetime,timezone
from typing import List

from app.db.session import get_db
from app.schemas import schemas
from app.crud import user
from app.core import security
from app.crud.auth import revoke_token


router = APIRouter()


@router.post("/",response_model=schemas.UserResponse)
def user_create(user_data:schemas.UserCreate,db:Session = Depends(get_db)):
    return user.create_user(db=db,user=user_data)

@router.post("/logout")
def logout(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.jwt_manager.verify_token(db=db, token=token)
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    revoke_token(db=db, token_id=payload["jti"], expires_at=expires_at)
    return {"message": "Logged out successfully"}



lockRoutes = APIRouter(
    dependencies=[Depends(security.get_current_user)]
)



@lockRoutes.get("/",response_model=List[schemas.UserResponse])
def read_user(db:Session = Depends(get_db)):
    return user.get_users(db=db)

