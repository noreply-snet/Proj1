from typing import List, Optional
from pydantic import BaseModel


# Base schema for Permission
class PermissionBase(BaseModel):
    name: str

# Schema for creating a Permission
class PermissionCreate(PermissionBase):
    pass

# Schema for Permission response
class PermissionResponse(PermissionBase):
    id: int

    class Config:
        from_attributes = True


# Base schema for Role
class RoleBase(BaseModel):
    name: str

# Schema for creating a Role
class RoleCreate(RoleBase):
    pass

# Schema for Role response
class RoleResponse(RoleBase):
    id: int
    permissions: Optional[List[PermissionBase]] = []

    class Config:
        from_attributes = True