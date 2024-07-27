from pydantic import BaseModel
from typing import List, Optional



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
        from_attributes = True






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
        from_attributes = True
        



class UserBase(BaseModel):
    name: Optional[str] = None
    username: str

class UserUsername(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Token1(BaseModel):
    token: str