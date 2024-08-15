from fastapi import FastAPI
from app.db.session import engine, Base
from app.api import students, cources, token, user
from threading import Thread
from app.services.schedule_task import run_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()



app.include_router(students.router, prefix="/student", tags=["student"])
app.include_router(cources.router, prefix="/course", tags=["course"])
app.include_router(token.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(user.lockRoutes, prefix="/lock", tags=["lock_user"])
