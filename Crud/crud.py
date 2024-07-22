from sqlalchemy.orm import Session
from DB import models,schemas

def create_student(db:Session, student:schemas.StudentCreate):
    db_student = models.Student(name = student.name, std_id = student.std_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def create_course(db:Session, course:schemas.CourseCreate):
    db_course = models.Course(course_name = course.course_name, course_id = course.course_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def linl_student_course(db:Session, student_id:str,course_id:str):
    db_student = db.query(models.Student).filter(models.Student.std_id == student_id).first()
    db_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()

    if not db_student or not db_course:
        return None
    db_student.courses.append(db_course)
    db.commit()
    return db_student

def get_student(db: Session):
    students = db.query(models.Student).all()

    return[
        schemas.StudentResponse(
            name = student.name,
            std_id = student.std_id,
            courses = [course.course_id for course in student.courses]
        ) for student in students 
    ]

def get_course(db: Session):
    courses = db.query(models.Course).all()

    return [
        schemas.CourseResponse(
            course_id = course.course_id,
            course_name = course.course_name,
            students = [student.std_id for student in course.students]
        ) for course in courses 
    ]