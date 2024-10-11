from uuid import UUID
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException

from services.courses_service.courses_create import CourseCreate
from models import Course
from services.courses_service.courses_repository import create_course, fetch_courses, find_course_by_id


def create_course_service(course_data: CourseCreate, db: Session):
    try:
        # Creating a new course instance
        new_course = Course(
            id=uuid4(),
            name=course_data.name,
            instructor=course_data.instructor,
            credits=course_data.credits
        )

        # Save the new course to the database
        saved_course = create_course(new_course, db)

        # Response Obj
        response_data = {
            "name": saved_course.name,
            "instructor": saved_course.instructor,
            "credits": saved_course.credits
        }

        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def fetch_courses_service(limit: int = 10, offset: int = 0, db: Session = None):
    try:
        courses = fetch_courses(
            limit=limit,
            offset=offset,
            db=db
        )
        return [

            {
                "name": course.name,
                "instructor": course.instructor,
                "credits": course.credits
            }
            for course in courses
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )


def fetch_course_by_id_service(course_id: UUID, db: Session):
    try:
        course = find_course_by_id(
            course_id=course_id,
            db=db
        )
        if course is None:
            raise HTTPException(
                status_code=404,
                detail="A Course with this id not found"
            )

        # Response Obj
        response_data = {
            "name": course.name,
            "instructor": course.instructor,
            "credits": course.credits
        }

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
