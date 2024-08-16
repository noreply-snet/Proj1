from sqlalchemy.orm import Session
from app.schemas import schemas
from app.models import models
from app.services.hashing import hash_password

# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

# Get all users
def get_users(db: Session):
    users = db.query(models.Users).all()
    return [
        schemas.UserResponse(
            name=user.name,
            username=user.username,
            role=user.role.name  # Include the role in the response
        ) for user in users
    ]

# Create a new user with a role
def create_user(db: Session, user: schemas.UserCreate, role_name: str):
    password = hash_password(user.password)
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist")

    db_user = models.Users(
        username=user.username,
        name=user.name,
        hashed_password=password,
        role_id=role.id  # Assign the role to the user
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Assign a role to a user
def assign_role_to_user(db: Session, username: str, role_name: str):
    user = get_user_by_username(db, username)
    if not user:
        raise ValueError(f"User '{username}' does not exist")
    
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist")

    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return user

# Get user by ID with role
def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        return schemas.UserResponse(
            name=user.name,
            username=user.username,
            role=user.role.name  # Include the role in the response
        )
    return None
