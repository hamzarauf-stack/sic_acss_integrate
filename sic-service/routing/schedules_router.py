from typing import List
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from db import get_db
from sqlalchemy.orm import Session

from services.schedules_service.schedule_create import ScheduleCreate
from services.schedules_service.schedules_response import ScheduleItem
from services.schedules_service.schedules_service import create_schedule_service, fetch_schedules_service, find_schedules_by_course, create_schedules_recieved
from auth_dependency.auth_verify import get_current_user

router = APIRouter()


@router.get("/")
def get_schedules(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return fetch_schedules_service(
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


@router.post("/")
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    return create_schedule_service(schedule, db)


@router.post("/schedules_recieve")
def fetch_schedule(schedules_data: List[ScheduleItem], db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    return create_schedules_recieved(
        schedules_data=schedules_data,
        db=db
    )
