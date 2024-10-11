from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db
from services.schedules_service.schedules_create import ScheduleCreate
from services.schedules_service.schedules_service import fetch_schedules_by_courses_service, find_schedules_by_course, create_schedule_service, fetch_send_schedules_service
from auth_dependency.auth_verify import get_current_user

router = APIRouter()


@router.get("/")
def get_schedules(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return fetch_schedules_by_courses_service(
        limit=limit,
        offset=offset,
        db=db
    )


@router.get("/{course_id}")
def get_schedules_by_course(course_id: UUID, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return find_schedules_by_course(
        course_id=course_id,
        db=db,
        limit=limit,
        offset=offset
    )


@router.post("/", response_model=ScheduleCreate)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    return create_schedule_service(schedule, db)


@router.post("/send_schedules")
def send_schedules(db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    return fetch_send_schedules_service(
        db=db,
        user_data=user_data
    )
