from sqlalchemy.orm import Session
from app.models import user_models
from app.schemas import role_permit


# CRUD operations for Role
def create_role(db: Session, role: role_permit.RoleCreate):
    db_role = user_models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_role(db: Session, role_id: int):
    role = db.query(user_models.Role).filter(user_models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role or Permission not found")
    return role

def get_roles(db: Session):
    return db.query(user_models.Role).all()

def delete_role(db: Session, role_id: int):
    role = db.query(user_models.Role).filter(user_models.Role.id == role_id).first()
    if role:
        db.delete(role)
        db.commit()
        return True
    return False


# CRUD operations for Permission
def create_permission(db: Session, permission: role_permit.PermissionCreate):
    db_permission = user_models.Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_permission(db: Session, permission_id: int):
    return db.query(user_models.Permission).filter(user_models.Permission.id == permission_id).first()

def get_permissions(db: Session):
    return db.query(user_models.Permission).all()

def delete_permission(db: Session, permission_id: int):
    permission = db.query(user_models.Permission).filter(user_models.Permission.id == permission_id).first()
    if permission:
        db.delete(permission)
        db.commit()
        return True
    return False

# Assign a permission to a role
def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    role = get_role(db, role_id)
    permission = get_permission(db, permission_id)
    if role and permission:
        role.permissions.append(permission)
        db.commit()
        db.refresh(role)
        return role
    return None


