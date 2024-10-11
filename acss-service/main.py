from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from db import engine
import logging

from routing import courses_router
from routing import rooms_router
from routing import schedules_router
from routing import enrollments_router

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


# Include Routers
app.include_router(courses_router.router,
                   prefix="/api/micro-acss/courses", tags=["Courses"])
app.include_router(rooms_router.router,
                   prefix="/api/micro-acss/rooms", tags=["Rooms"])
app.include_router(schedules_router.router,
                   prefix="/api/micro-acss/schedules", tags=["Schedules"])
app.include_router(enrollments_router.router,
                   prefix="/api/micro-acss/enrollments", tags=["enrollments"])
