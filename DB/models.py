from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .db import Base


student_course_link = Table(
    'student_course_link',
    Base.metadata,
    Column('student_id',String, ForeignKey('students.std_id')),
    Column('course_id',String, ForeignKey('courses.course_id'))
)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    std_id = Column(String,unique=True)
    courses = relationship("Course", secondary=student_course_link, back_populates="students")


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True,index=True)
    course_name = Column(String)
    course_id = Column(String,unique=True)
    students = relationship("Student", secondary=student_course_link, back_populates="courses")

