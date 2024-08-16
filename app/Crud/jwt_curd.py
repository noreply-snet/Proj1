from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.models.jwt_models import RevokedToken
from datetime import datetime, timezone
from app.services.common import convert_utc_to_ist


def revoke_token(db: Session, token_id: str, expires_at: datetime):
    revoked_token = RevokedToken(token_id=token_id, expires_at=expires_at)
    db.add(revoked_token)
    db.commit()

def is_token_revoked(db: Session, token_id: str):
    return db.query(RevokedToken).filter(RevokedToken.token_id == token_id).first() is not None




def get_expired_tokens(db: Session):
    tokens = db.query(RevokedToken).all()

    return [
        RevokedToken(
            token_id=token.token_id,
            revoked_at=convert_utc_to_ist(token.revoked_at),
            expires_at=convert_utc_to_ist(token.expires_at),
        ) for token in tokens
    ]


def cleanup_expired_tokens(db: Session):
    now = datetime.now(timezone.utc)
    db.execute(
        delete(RevokedToken).where(RevokedToken.expires_at < now)
    )
    db.commit()  # Commit the transaction
