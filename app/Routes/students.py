from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..DB import db,schemas
from ..Crud import crud
from typing import List

router = APIRouter()

@router.post("/",response_model=schemas.StudentResponse)
def student_create(student:schemas.StudentCreate,db:Session = Depends(db.get_db)):
    return crud.create_student(db=db,student=student)


@router.get("/",response_model=List[schemas.StudentResponse])
def read_student(db:Session = Depends(db.get_db)):
    return crud.get_student(db=db)

@router.post("/{std_id}/course/{course_id}")
def link_student_to_course(std_id:str,course_id:str,db:Session = Depends(db.get_db)):
    result =  crud.linl_student_course(db=db,student_id=std_id,course_id=course_id)
    if not result:
        raise HTTPException(status_code=404, detail="Author or Book not found")
    return {"message": "Author and book linked"}