from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging

from services.schedules_service.schedules_response import ScheduleItem
from services.schedules_service.schedule_create import ScheduleCreate
from models import Schedule
from services.schedules_service.schedules_repository import create_schedule, fetch_schedules, find_schedules_by_course, find_schedules_by_courses_all
from services.courses_service.courses_repository import find_course_by_id

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

        # Creating a new schedule instance
        new_schedule = Schedule(
            course_id=UUID(schedule_data.course_id),
            room=schedule_data.room,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
            day_of_week=schedule_data.day_of_week
        )

        # Save the new Schedule to the database
        saved_schedule = create_schedule(new_schedule, db)

        # Response Obj
        response_data = {
            "course_id": str(saved_schedule.course_id),
            "room": saved_schedule.room,
            "start_time": saved_schedule.start_time,
            "end_time": saved_schedule.end_time,
            "day_of_week": saved_schedule.day_of_week
        }

        return response_data

    except (Exception, ValueError) as e:
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
                "room": schedule.room,
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
            course_id=course_id,
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
                "course_id": str(schedule.course_id),
                "room": schedule.room,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "day_of_week": schedule.day_of_week
            }
            for schedule in schedules
        ]

    except Exception as e:
        raise e


def create_schedules_recieved(schedules_data: List[ScheduleItem], db: Session):
    # to prevent circular import
    from models import Course
    from models import Schedule
    from services.courses_service.courses_repository import create_course

    # # Hashmap to keep track of courses that have been created
    created_courses = {}

    # Persisting course schedules
    try:
        for schedule in schedules_data:

            logger.info("Data Persistance Started")

            # Creating the course
            if schedule.course.id not in created_courses:
                new_course = Course(
                    id=schedule.course.id,
                    name=schedule.course.name,
                    instructor=schedule.course.instructor,
                    credits=schedule.course.credits
                )
                create_course(
                    course=new_course,
                    db=db
                )
                created_courses[schedule.course.id] = True

            # Creating the schedule
            new_schedule = Schedule(
                course_id=schedule.course.id,
                room=schedule.rooms.name,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                day_of_week=schedule.day_of_week
            )
            create_schedule(
                schedule=new_schedule,
                db=db
            )

        logger.info("Data Persisted")

        # Fetching the persisted data
        schedules = find_schedules_by_courses_all(db=db)

        schedules_json = [

            {
                "course_id": str(schedule.course_id),
                "room": schedule.room,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "day_of_week": schedule.day_of_week
            }
            for schedule in schedules
        ]

        return {
            "status": 200,
            "response": schedules_json,
            "response_text": "Data Persisted"
        }

    except Exception as e:
        raise e
