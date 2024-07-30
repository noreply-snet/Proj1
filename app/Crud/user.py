from sqlalchemy.orm import Session
from app.schemas import schemas
from app.models import models
from app.services.hashing import hash_password


def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def get_users(db: Session):
    users = db.query(models.Users).all()

    return [
        schemas.UserResponse(
            name = user.name,
            username = user.username,
        ) for user in users 
    ]

def create_user(db: Session, user: schemas.UserCreate):
    password = hash_password(user.password)
    db_user = models.Users(
        username=user.username, name=user.name, hashed_password=password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
