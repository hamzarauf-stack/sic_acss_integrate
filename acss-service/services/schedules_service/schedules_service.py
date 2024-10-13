from uuid import UUID
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException
import requests
import logging

from services.schedules_service.schedules_create import ScheduleCreate
from models import Schedule
from services.schedules_service.schedules_repository import find_schedules_by_course, create_schedule, fetch_schedules, find_schedules_by_courses, find_schedules_by_courses_all
from services.courses_service.courses_repository import find_course_by_id
from services.rooms_service.rooms_repository import find_room_by_id

logger = logging.getLogger(__name__)


def create_schedule_service(schedule_data: ScheduleCreate, db: Session):
    try:

        # Checking Course exists or not
        course = find_course_by_id(
            course_id=schedule_data.course_id,
            db=db
        )
        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course with this ID don't exists"
            )

        # Checking room exists or not
        room = find_room_by_id(
            room_id=schedule_data.room_id,
            db=db
        )
        if room is None:
            raise HTTPException(
                status_code=404,
                detail="Room with this ID don't exists"
            )

        # Creating a new schedule instance
        new_schedule = Schedule(
            id=uuid4(),
            course_id=UUID(schedule_data.course_id),
            room_id=UUID(schedule_data.room_id),
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
            day_of_week=schedule_data.day_of_week
        )

        # Save the new Schedule to the database
        saved_schedule = create_schedule(new_schedule, db)

        # Response Obj
        response_data = {
            "course_id": str(saved_schedule.course_id),
            "room_id": str(saved_schedule.room_id),
            "start_time": saved_schedule.start_time,
            "end_time": saved_schedule.end_time,
            "day_of_week": saved_schedule.day_of_week
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def fetch_schedules_service(limit: int = 10, offset: int = 0, db: Session = None):
    try:
        schedules = fetch_schedules(
            limit=limit,
            offset=offset,
            db=db
        )
        return [

            {
                "course_id": str(schedule.course_id),
                "room": str(schedule.room_id),
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "day_of_week": schedule.day_of_week
            }
            for schedule in schedules
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )


def fetch_schedules_by_course_service(course_id: UUID, db: Session, limit: int, offset: int):
    try:
        # Checking Course exists or not
        course = find_course_by_id(
            course_id=str(course_id),
            db=db
        )
        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course with this ID don't exists"
            )

        # Fetching schedules by course
        schedules = find_schedules_by_course(
            course_id=course_id,
            db=db,
            limit=limit,
            offset=offset
        )

        return [

            {
                "schedule_id": str(schedule.id),
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "day_of_week": schedule.day_of_week,
                "courses": schedule.courses,
                "rooms": schedule.rooms
            }
            for schedule in schedules
        ]

    except Exception as e:
        logger.error('Error: %s', e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def fetch_schedules_by_courses_service(db: Session, limit: int, offset: int):
    try:
        # Fetching schedules by course
        schedules = find_schedules_by_courses(
            db=db,
            limit=limit,
            offset=offset
        )

        return [

            {
                "course": schedule.courses,
                "rooms": schedule.rooms,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "day_of_week": schedule.day_of_week
            }
            for schedule in schedules
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )


def fetch_send_schedules_service(db: Session, user_data: dict):
    try:
        schedules = find_schedules_by_courses_all(
            db=db
        )
        # Schedules Object formation
        schedules_obj = [
            {
                "course": {
                    "id": str(schedule.courses.id),
                    "name": schedule.courses.name,
                    "instructor": schedule.courses.instructor,
                    "credits": schedule.courses.credits
                },
                "rooms": {
                    "id": str(schedule.rooms.id),
                    "name": schedule.rooms.name,
                    "capacity": schedule.rooms.capacity
                },
                "start_time": str(schedule.start_time),
                "end_time": str(schedule.end_time),
                "day_of_week": schedule.day_of_week,
                "id": str(schedule.id)
            }
            for schedule in schedules
        ]

        # Calling api to send schedules
        response = requests.post(
            url="http://sic_service:8000/api/micro-sci/schedules/schedules_recieve/",
            json=schedules_obj,
            headers={
                "Authorization": f"Bearer {user_data.get('token')}"
            }
        )
        response.raise_for_status()

        return {
            "status": 200,
            "response": response.json()
        }

    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
