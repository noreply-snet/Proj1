from sqlalchemy.orm import Session
from app.schemas import std_course
from app.models import user_models

# Student CRUD Operations
def create_student(db: Session, student: std_course.StudentCreate):
    db_student = user_models.Student(name=student.name, std_id=student.std_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: str, student: std_course.StudentCreate):
    db_student = db.query(user_models.Student).filter(user_models.Student.std_id == student_id).first()
    if db_student:
        db_student.name = student.name
        db.commit()
        db.refresh(db_student)
        return db_student
    return None

def delete_student(db: Session, student_id: str):
    db_student = db.query(user_models.Student).filter(user_models.Student.std_id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

def get_student(db: Session):
    students = db.query(user_models.Student).all()
    return [
        std_course.StudentResponse(
            name=student.name,
            std_id=student.std_id,
            courses=[course.course_id for course in student.courses]
        ) for student in students
    ]

# Course CRUD Operations
def create_course(db: Session, course: std_course.CourseCreate):
    db_course = user_models.Course(course_name=course.course_name, course_id=course.course_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: str, course: std_course.CourseCreate):
    db_course = db.query(user_models.Course).filter(user_models.Course.course_id == course_id).first()
    if db_course:
        db_course.course_name = course.course_name
        db.commit()
        db.refresh(db_course)
        return db_course
    return None

def delete_course(db: Session, course_id: str):
    db_course = db.query(user_models.Course).filter(user_models.Course.course_id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return True
    return False

def get_course(db: Session):
    courses = db.query(user_models.Course).all()
    return [
        std_course.CourseResponse(
            course_id=course.course_id,
            course_name=course.course_name,
            students=[student.std_id for student in course.students]
        ) for course in courses
    ]

def linl_student_course(db:Session, student_id:str,course_id:str):
    db_student = db.query(user_models.Student).filter(user_models.Student.std_id == student_id).first()
    db_course = db.query(user_models.Course).filter(user_models.Course.course_id == course_id).first()

    if not db_student or not db_course:
        return None
    db_student.courses.append(db_course)
    db.commit()
    return db_student

