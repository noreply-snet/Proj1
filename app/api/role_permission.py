from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import role_permit
from app.crud import role_crud,user_crud
from app.schemas import user_sch
from app.db.session import get_db
from typing import List

router = APIRouter()

# Role Endpoints

@router.post("/roles/", response_model=role_permit.RoleResponse)
def create_role(role: role_permit.RoleCreate, db: Session = Depends(get_db)):
    return role_crud.create_role(db=db, role=role)

@router.get("/roles/{role_id}", response_model=role_permit.RoleResponse)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = role_crud.get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.get("/roles/", response_model=List[role_permit.RoleResponse])
def read_roles(db: Session = Depends(get_db)):
    return role_crud.get_roles(db=db)

@router.delete("/roles/{role_id}", status_code=status.HTTP_200_OK)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    if not role_crud.delete_role(db=db, role_id=role_id):
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "deleted successfully"} 

# Permission Endpoints

@router.post("/permissions/", response_model=role_permit.PermissionResponse)
def create_permission(permission: role_permit.PermissionCreate, db: Session = Depends(get_db)):
    return role_crud.create_permission(db=db, permission=permission)

@router.get("/permissions/{permission_id}", response_model=role_permit.PermissionResponse)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = role_crud.get_permission(db=db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.get("/permissions/", response_model=List[role_permit.PermissionResponse])
def read_permissions(db: Session = Depends(get_db)):
    return role_crud.get_permissions(db=db)

@router.delete("/permissions/{permission_id}", status_code=status.HTTP_200_OK)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    if not role_crud.delete_permission(db=db, permission_id=permission_id):
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "deleted successfully"}



#////////////////////////////////
# Endpoint to assign a permission to a role
@router.post("/roles/{role_id}/permissions/{permission_id}", response_model=role_permit.RoleResponse)
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = role_crud.assign_permission_to_role(db=db, role_id=role_id, permission_id=permission_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role or Permission not found")
    return role

# Endpoint to assign a permission to a user
@router.post("/users/{username}/permissions/{permission_name}", response_model=user_sch.UserResponse)
def assign_permission_to_user(username: str, permission_name: str, db: Session = Depends(get_db)):
    try:
        user = user_crud.assign_permission_to_user(db=db, username=username, permission_name=permission_name)
        return user  # Return the updated user response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle errors
