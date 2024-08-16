from sqlalchemy.orm import Session
from app.schemas import user_sch
from app.models import user_models
from app.services.hashing import hash_password

# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(user_models.Users).filter(user_models.Users.username == username).first()

# Get all users
def get_users(db: Session):
    users = db.query(user_models.Users).all()
    return [
        user_sch.UserResponse(
            name=user.name,
            username=user.username,
            role=user.role.name  # Include the role in the response
        ) for user in users
    ]

# Create a new user with a role
def create_user(db: Session, user: user_sch.UserCreate):
    password = hash_password(user.password)
    role = db.query(user_models.Role).filter(user_models.Role.name == user.role_name).first()
    
    if not role:
        raise ValueError(f"Role '{user.role_name}' does not exist")

    db_user = user_models.User(
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
    
    role = db.query(user_models.Role).filter(user_models.Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist")

    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return user

# Get user by ID with role
def get_user_by_id(db: Session, user_id: int):
    user = db.query(user_models.Users).filter(user_models.Users.id == user_id).first()
    if user:
        return user_sch.UserResponse(
            name=user.name,
            username=user.username,
            role=user.role.name  # Include the role in the response
        )
    return None
