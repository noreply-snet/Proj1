from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import uuid

from app.schemas.auth_schemas import JWTPayload
from app.crud.jwt_curd import is_token_revoked
from app.crud.user_crud import get_user_by_username
from app.core.config import settings


class JWTManager:
    def generate_tokens(self, username: str):
        jwt_id = str(uuid.uuid4())
        access_token = self.create_token(
            data={"sub": username}, token_type="access", jwi=jwt_id
        )
        refresh_token = self.create_token(
            data={"sub": username}, token_type="refresh", jwi=jwt_id
        )
        return access_token, refresh_token

    @staticmethod
    def create_token(data: dict, token_type: str, jwi: str = None) -> str:
        to_encode = data.copy()
        if token_type == "access":
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_EXPIRE)
        elif token_type == "refresh":
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_EXPIRE)
        else:
            raise ValueError("Invalid token type. Must be 'access' or 'refresh'.")
        
        to_encode.update({"exp": expire, "jti": jwi})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET, algorithm=settings.ALGO)
        return encoded_jwt

    def verify_token(self, db: Session, token: str):  # Ensure self is the first parameter
        excp = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGO])
            
            if is_token_revoked(db, payload["jti"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            if "exp" in payload and datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            username: str = payload.get("sub")
            if username is None:
                raise excp

            return payload  # Return the payload
        except JWTError:
            raise excp

    def get_user_from_payload(self, db: Session, payload: JWTPayload):  # Ensure self is the first parameter
        username: str = payload.get("sub")
        user = get_user_by_username(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user  # Return the user



jwt_manager = JWTManager()  # Create an instance of JWTManager