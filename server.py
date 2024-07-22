from fastapi import FastAPI
from DB.db import engine,Base
from Routes import students,cources

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(students.router,prefix="/student",tags=["student"])
app.include_router(cources.router,prefix="/course",tags=["course"])

