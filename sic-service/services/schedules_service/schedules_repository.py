from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models import Schedule


def create_schedule(schedule: Schedule, db: Session):
    db.add(schedule)
    try:
        db.commit()
        # Refresh to get the newly created schedule's data from the DB
        db.refresh(schedule)
        return schedule
    except Exception as e:
        db.rollback()
        raise e


def fetch_schedules(db: Session, limit: int = 10, offset: int = 0) -> List[Schedule]:
    from models import Course
    schedules = db.query(Schedule).join(Course, Schedule.course_id == Course.id).options(
        joinedload(Schedule.course)).limit(limit).offset(offset).all()
    return schedules


def find_schedule_by_id(schedule_id: UUID, db: Session):
    schedule = db.query(Schedule).filter(
        Schedule.id == UUID(schedule_id)).first()
    return schedule


def find_schedules_by_course(course_id: UUID, db: Session, limit: int = 10, offset: int = 0):

    from models import Course
    schedules = (
        db.query(Schedule).join(Course, Schedule.course_id == course_id).filter(
            Schedule.course_id == course_id).options(joinedload(Schedule.course)).limit(limit).offset(offset).all()
    )
    return schedules


def find_schedules_by_courses_all(db: Session):

    from models import Course
    schedules = (
        db.query(Schedule).join(
            Course, Schedule.course_id == Course.id).all()
    )
    return schedules
