from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine, Base , get_db
from app.api import students, token, user , role_permission
from threading import Thread
from app.services.schedule_task import run_scheduler
from app.services.basic_db_setup import create_roles_and_permissions
from pathlib import Path


Base.metadata.create_all(bind=engine)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here
    print("Application startup")

    create_roles_and_permissions()

    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    yield  # Yield control back to FastAPI
    
    # Shutdown logic here
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)



app.include_router(students.router, prefix="/student", tags=["Student"])
app.include_router(token.router, prefix="/auth", tags=["Tokens"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(user.lockRoutes, prefix="/lock", tags=["Lock Routes"])
app.include_router(role_permission.router, prefix="/permit", tags=["Roles and Permissions"])

predefined_roles = [
    {"name": "Admin", "permissions": ["read_user", "write_user", "delete_user"]},
    {"name": "Editor", "permissions": ["read_user", "write_user"]},
    {"name": "Visitor", "permissions": ["read_user"]},
]