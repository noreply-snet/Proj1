from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine, Base
from app.api import students, cources, token, user
from threading import Thread
from app.services.schedule_task import run_scheduler
from pathlib import Path


Base.metadata.create_all(bind=engine)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here
    print("Application startup")
    
    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Yield control back to FastAPI
    yield
    
    # Shutdown logic here
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)



app.include_router(students.router, prefix="/student", tags=["student"])
app.include_router(cources.router, prefix="/course", tags=["course"])
app.include_router(token.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(user.lockRoutes, prefix="/lock", tags=["lock_user"])
