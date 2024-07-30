from pydantic import BaseModel
from datetime import datetime

class JWTPayload(BaseModel):
    sub: str
    exp: datetime
    jti: str
