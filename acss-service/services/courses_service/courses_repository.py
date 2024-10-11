from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from models import Course


def create_course(course: Course, db: Session):
    db.add(course)
    try:
        db.commit()
        # Refresh to get the newly created course's data from the DB
        db.refresh(course)
        return course
    except Exception as e:
        db.rollback()
        raise e


def fetch_courses(db: Session, limit: int = 10, offset: int = 0) -> List[Course]:
    try:
        courses = db.query(Course).limit(limit).offset(offset).all()
        return courses
    except Exception as e:
        raise e


def find_course_by_id(course_id: UUID, db: Session):
    try:
        course = db.query(Course).filter(
            Course.id == UUID(course_id)).first()
        return course
    except Exception as e:
        raise e
