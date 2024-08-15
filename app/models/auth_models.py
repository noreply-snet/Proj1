from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from app.db.session import Base

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'
    
    token_id = Column(String, primary_key=True, index=True)
    revoked_at = Column(DateTime,default=lambda: datetime.now(timezone.utc))  # Ensure timezone-aware
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<RevokedToken(token_id={self.token_id}, expires_at={self.expires_at})>"