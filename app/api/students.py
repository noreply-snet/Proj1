from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas import schemas
from app.crud import student_course

router = APIRouter()

@router.post("/",response_model=schemas.StudentResponse)
def student_create(student:schemas.StudentCreate,db:Session = Depends(get_db)):
    return student_course.create_student(db=db,student=student)


@router.get("/",response_model=List[schemas.StudentResponse])
def read_student(db:Session = Depends(get_db)):
    return student_course.get_student(db=db)

@router.post("/{std_id}/course/{course_id}")
def link_student_to_course(std_id:str,course_id:str,db:Session = Depends(get_db)):
    result =  student_course.linl_student_course(db=db,student_id=std_id,course_id=course_id)
    if not result:
        raise HTTPException(status_code=404, detail="Author or Book not found")
    return {"message": "Author and book linked"}