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
        



# Base schema for user-related data
class UserBase(BaseModel):
    name: Optional[str] = None
    username: str

# Schema for user creation (input)
class UserCreate(UserBase):
    password: str
    role_name: Optional[str] = None  # Add role_name to assign a role during user creation

# Schema for user response (output)
class UserResponse(UserBase):
    role: Optional[str] = None  # Include the user's role in the response

    class Config:
        from_attributes = True

# Schema for user username (simplified schema)
class UserUsername(BaseModel):
    username: str





class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Token1(BaseModel):
    token: str

