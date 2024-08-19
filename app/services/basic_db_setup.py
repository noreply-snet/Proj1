from app.core.config import predefined_roles
from app.models.user_models import Role,Permission,role_permission
from app.crud.role_crud import role_exists,permission_exists,create_permission,create_role,clear_role_permission_links, assign_permission_to_role
from app.schemas import role_permit
from app.db.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

# Function to create roles and permissions at startup
def create_roles_and_permissions(db: Session = next(get_db())):
    # Step 1: Add roles, checking if they already exist
    for role_data in predefined_roles:
        if not role_exists(db, role_data["role_name"]):
            new_role = role_permit.RoleCreate(name=role_data["role_name"])
            create_role(db, new_role)
    
    # Step 2: Add permissions, checking if they already exist
    for role_data in predefined_roles:
        for perm_name in role_data["permissions"]:
            if not permission_exists(db, perm_name):
                new_permission = role_permit.PermissionCreate(name=perm_name)
                create_permission(db, new_permission)
    
    # Step 3: Clear the role-permission link table
    clear_role_permission_links(db)

    # Step 4: Establish relationships between roles and permissions
    for role_data in predefined_roles:
        role = db.query(Role).filter(Role.name == role_data["role_name"]).first()
        for perm_name in role_data["permissions"]:
            permission = db.query(Permission).filter(Permission.name == perm_name).first()
            if permission and role:
                assign_permission_to_role(db, role.id, permission.id)