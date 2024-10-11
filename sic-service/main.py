from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from db import engine
import logging

from routing import courses_router
from routing import users_router
from routing import students_router
from routing import enrollments_router
from routing import schedules_router

app = FastAPI()

logger = logging.getLogger()


@app.get("/")
def ping_db_conn():
    try:
        with engine.connect() as conn:
            conn.execute(select(1))
        return {"message": "Welcome to FastAPI", "db_connection": "successful"}
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(
            status_code=500, detail="Database connection failed")


# Include the Routers
app.include_router(users_router.router,
                   prefix="/api/micro-sci/users", tags=["Users"])
app.include_router(students_router.router,
                   prefix="/api/micro-sci/students", tags=["Students"])
app.include_router(courses_router.router,
                   prefix="/api/micro-sci/courses", tags=["Courses"])
app.include_router(enrollments_router.router,
                   prefix="/api/micro-sci/enrollments", tags=["Enrollments"])
app.include_router(schedules_router.router,
                   prefix="/api/micro-sci/schedules", tags=["Schedules"])
