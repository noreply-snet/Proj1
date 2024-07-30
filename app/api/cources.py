from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas import schemas
from app.crud import student_course


router = APIRouter()


@router.post("/",response_model=schemas.CourseCreate)
def create_courses(course:schemas.CourseCreate,db:Session= Depends(get_db)):
    return student_course.create_course(db=db,course=course)

@router.get("/",response_model=List[schemas.CourseResponse])
def get_courses(db:Session= Depends(get_db)):
    return student_course.get_course(db=db)
    