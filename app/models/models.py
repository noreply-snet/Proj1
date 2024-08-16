from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.db.session import Base


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



# Association table for many-to-many relationship between roles and permissions
role_permission = Table(
    'role_permission', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role")
