from sqlalchemy.orm import Session
from app.DB import models,schemas
from app.Auth.security import pwd_context






def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    users = db.query(models.Users).offset(skip).limit(limit).all()

    return [
        schemas.UserResponse(
            name = user.name,
            username = user.username,
        ) for user in users 
    ]

def create_user(db: Session, user: schemas.UserCreate):
    password = pwd_context.hash(user.password)
    db_user = models.Users(
        username=user.username, name=user.name, hashed_password=password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
