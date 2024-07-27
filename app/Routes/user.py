from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.DB import db,schemas
from app.Crud import user_crud
from app.Auth import security
from typing import List,Optional

router = APIRouter()

@router.post("/",response_model=schemas.UserResponse)
def user_create(user_data:schemas.UserCreate,db:Session = Depends(db.get_db)):
    return user_crud.create_user(db=db,user=user_data)






lockRoutes = APIRouter(
    dependencies=[Depends(security.get_current_user)]
)






@lockRoutes.get("/",response_model=List[schemas.UserResponse])
def read_user(db:Session = Depends(db.get_db)):
    return user_crud.get_users(db=db)