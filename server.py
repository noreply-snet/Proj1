from fastapi import FastAPI
from app.DB.db import engine,Base
from app.Routes import students,cources,token,user


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(students.router,prefix="/student",tags=["student"])
app.include_router(cources.router,prefix="/course",tags=["course"])
app.include_router(token.router,prefix="/auth",tags=["auth"])
app.include_router(user.router,prefix="/user",tags=["user"])
app.include_router(user.lockRoutes,prefix="/user",tags=["lock_user"])

