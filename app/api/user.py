import shutil
from fastapi import APIRouter,Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime,timezone
from typing import List
from pathlib import Path

from app.db.session import get_db
from app.schemas import user_sch
from app.crud import user_crud
from app.core import security
from app.crud.jwt_curd import revoke_token
from app.models.user_models import Role

router = APIRouter()

UPLOAD_DIR = Path("uploads")

@router.post("/",response_model=user_sch.UserCreate)
def user_create(user_data:user_sch.UserCreate,db:Session = Depends(get_db)):
    return user_crud.create_user(db=db,user=user_data)

@router.post("/logout")
def logout(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.jwt_manager.verify_token(db=db, token=token)
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    revoke_token(db=db, token_id=payload["jti"], expires_at=expires_at)
    return {"message": "Logged out successfully"}



lockRoutes = APIRouter(
    dependencies=[Depends(security.get_current_user)]
)



@lockRoutes.get("/",response_model=List[user_sch.UserResponse])
def read_user(db:Session = Depends(get_db)):
    return user_crud.get_users(db=db)


@lockRoutes.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = UPLOAD_DIR / file.filename
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@lockRoutes.get("/files/{filename}")
async def get_file(filename: str):
    file_location = UPLOAD_DIR / filename
    if not file_location.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_location)

@lockRoutes.get("/admin-dashboard")
async def admin_dashboard(
    role_check: Role = Depends(security.role_checker(["Admin"]))
):
    return {"message": "Welcome to the -> -> -> Admin dashboard"}

@lockRoutes.get("/editor-page")
async def editor_page(
    role_check: Role = Depends(security.role_checker(["Admin","Editor"]))
):
    return {"message": "Welcome to the -> -> Editor page"}

@lockRoutes.get("/visitor-page")
async def editor_page(
    role_check: Role = Depends(security.role_checker(["Admin","Editor","Visitor"]))
):
    return {"message": "Welcome to the -> Visitor page"}

@lockRoutes.get("/has-permission-page")
async def editor_page(
    role_check: Role = Depends(security.permission_checker("read_user"))
):
    return {"message": "Welcome to the -> Read_User permissionm page"}