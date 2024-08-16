import shutil
from fastapi import APIRouter,Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime,timezone
from typing import List
from pathlib import Path

from app.db.session import get_db
from app.schemas import schemas
from app.crud import user
from app.core import security
from app.crud.auth import revoke_token


router = APIRouter()

UPLOAD_DIR = Path("uploads")

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