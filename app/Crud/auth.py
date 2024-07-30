from sqlalchemy.orm import Session
from app.models.auth_models import RevokedToken
from datetime import datetime


def revoke_token(db: Session, token_id: str, expires_at: datetime):
    revoked_token = RevokedToken(token_id=token_id, expires_at=expires_at)
    db.add(revoked_token)
    db.commit()

def is_token_revoked(db: Session, token_id: str):
    return db.query(RevokedToken).filter(RevokedToken.token_id == token_id).first() is not None