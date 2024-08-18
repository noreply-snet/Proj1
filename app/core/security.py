from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.services.hashing import verify_password
from app.services.jwt import jwt_manager
from app.crud import user_crud
from app.db.session import get_db
from app.models.user_models import User, Role, Permission

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Authenticate the user by verifying the password
def authenticate_user(db: Session, username: str, password: str):
    user = user_crud.get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Get the current user from the token
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt_manager.verify_token(db=db, token=token)
    return jwt_manager.get_user_from_payload(db=db, payload=payload)

# Get the role of the current user
def get_user_role(current_user: User = Depends(get_current_user)):
    return current_user.role

# Check if the current user has any of the required roles
def role_checker(required_roles: list[str]):
    def role_dependency(role: Role = Depends(get_user_role)):
        if role.name not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
    return role_dependency

# Check if the current user has the required permission
def permission_checker(required_permission: str):
    def permission_dependency(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

        # Fetch all permissions associated with the user's have
        permissions = [permission.name for permission in current_user.permissions]
        if required_permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
    return permission_dependency
