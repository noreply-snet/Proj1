from pydantic import BaseModel
from typing import List

class StudentBase(BaseModel):
    name: str
    std_id: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    std_id: str
    name: str
    courses: List[str] = []

    class Config:
        orm_mode = True






class CourseBase(BaseModel):
    course_name : str
    course_id: str

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    course_id: str
    course_name: str
    students: List[str] = []

    class Config:
        orm_mode = True
