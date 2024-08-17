from sqlalchemy.orm import Session
from app.schemas import user_sch
from app.models import user_models
from app.services.hashing import hash_password
from app.crud.role_crud import get_role



# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(user_models.User).filter(user_models.User.username == username).first()

# Get all users
def get_users(db: Session):
    users = db.query(user_models.User).all()
    return [
        user_sch.UserResponse(
            name=user.name,
            username=user.username,
            role=get_role(db=db, role_id=user.role_id).name,  # Include detailed role information
            permissions=[perm.name for perm in user.permissions]  # Include permissions
        ) for user in users
    ]


def create_user(db: Session, user: user_sch.UserCreate):
    # Check if the username already exists
    existing_user = db.query(user_models.User).filter(user_models.User.username == user.username).first()
    if existing_user:
        raise ValueError(f"Username '{user.username}' already exists")
    
    # Hash the password
    password = hash_password(user.password)

    # Prevent creating SuperUser
    if user.role_name == 'SuperUser':
        raise ValueError("This Role cannot be assigned to a user")

    # Retrieve the role
    role = db.query(user_models.Role).filter(user_models.Role.name == user.role_name).first()
    if not role:
        raise ValueError(f"Role '{user.role_name}' does not exist")

    # Create a new user
    db_user = user_models.User(
        username=user.username,
        name=user.name,
        hashed_password=password,
        role_id=role.id  # Assign the role to the user
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Retrieve permissions associated with the user's role
    role_permissions = db.query(user_models.Permission).join(user_models.Role.permissions).filter(
        user_models.Role.id == role.id
    ).all()

    # Add role permissions to the user
    db_user.permissions.extend(role_permissions)

    # Create UserResponse with permissions
    return user_sch.UserResponse(
        name=db_user.name,
        username=db_user.username,
        role=get_role(db=db, role_id=db_user.role_id).name,  # Include detailed role information
        permissions=[perm.name for perm in db_user.permissions]  # Include permissions as PermissionBase instances
    )



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


# Get user by ID with role and permissions
def get_user_by_id(db: Session, user_id: int):
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if user:
        return user_sch.UserResponse(
            name=user.name,
            username=user.username,
            role=get_role(db=db, role_id=user.role_id).name,  # Include the role in the response
            permissions=[perm.name for perm in user.permissions]  # Include permissions
        )
    return None


# Assign a permission to a user
def assign_permission_to_user(db: Session, username: str, permission_name: str):
    user = get_user_by_username(db, username)
    if not user:
        raise ValueError(f"User '{username}' does not exist")
    
    permission = db.query(user_models.Permission).filter(user_models.Permission.name == permission_name).first()
    if not permission:
        raise ValueError(f"Permission '{permission_name}' does not exist")

    # Check if the user already has the permission
    if permission in user.permissions:
        raise ValueError(f"User '{username}' already has permission '{permission_name}'")

    user.permissions.append(permission)  # Add permission to user
    db.commit()  # Commit changes to the database
    db.refresh(user)  # Refresh the user object to reflect the new state

    return user_sch.UserResponse(
        name=user.name,
        username=user.username,
        role=get_role(db=db, role_id=user.role_id).name,  # Include detailed role information
        permissions=[perm.name for perm in user.permissions]  # Include permissions
    )