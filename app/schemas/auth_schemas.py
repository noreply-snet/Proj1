from pydantic import BaseModel
from datetime import datetime

class JWTPayload(BaseModel):
    sub: str
    exp: datetime
    jti: str

class RevokeToken(BaseModel):
    token_id: str
    revoked_at: datetime
    expires_at: datetime