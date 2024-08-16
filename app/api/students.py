from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas import std_course
from app.db.session import get_db
from app.crud import student_course

router = APIRouter()

# Student Operations
@router.post("/", response_model=std_course.StudentResponse)
def student_create(student: std_course.StudentCreate, db: Session = Depends(get_db)):
    return student_course.create_student(db=db, student=student)

@router.get("/", response_model=List[std_course.StudentResponse])
def read_student(db: Session = Depends(get_db)):
    return student_course.get_student(db=db)

@router.put("/{std_id}", response_model=std_course.StudentResponse)
def update_student(std_id: str, student: std_course.StudentCreate, db: Session = Depends(get_db)):
    db_student = student_course.update_student(db=db, student_id=std_id, student=student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/{std_id}", response_model=dict)
def delete_student(std_id: str, db: Session = Depends(get_db)):
    result = student_course.delete_student(db=db, student_id=std_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

# Course Operations
@router.post("/course/", response_model=std_course.CourseResponse)
def create_course(course: std_course.CourseCreate, db: Session = Depends(get_db)):
    return student_course.create_course(db=db, course=course)

@router.get("/course/", response_model=List[std_course.CourseResponse])
def read_courses(db: Session = Depends(get_db)):
    return student_course.get_course(db=db)

@router.put("/course/{course_id}", response_model=std_course.CourseResponse)
def update_course(course_id: str, course: std_course.CourseCreate, db: Session = Depends(get_db)):
    db_course = student_course.update_course(db=db, course_id=course_id, course=course)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.delete("/course/{course_id}", response_model=dict)
def delete_course(course_id: str, db: Session = Depends(get_db)):
    result = student_course.delete_course(db=db, course_id=course_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}

@router.post("/{std_id}/course/{course_id}")
def link_student_to_course(std_id: str, course_id: str, db: Session = Depends(get_db)):
    result = student_course.link_student_course(db=db, student_id=std_id, course_id=course_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    return {"message": "Student and course linked"}
