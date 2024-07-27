from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..DB import db,schemas
from ..Crud import crud
from typing import List


router = APIRouter()


@router.post("/",response_model=schemas.CourseCreate)
def create_courses(course:schemas.CourseCreate,db:Session= Depends(db.get_db)):
    return crud.create_course(db=db,course=course)

@router.get("/",response_model=List[schemas.CourseResponse])
def get_courses(db:Session= Depends(db.get_db)):
    return crud.get_course(db=db)
    