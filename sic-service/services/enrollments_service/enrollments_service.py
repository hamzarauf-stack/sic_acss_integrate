from uuid import UUID
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException
import requests
import logging

from services.enrollments_service.enrollment_create import EnrollmentCreate
from models import Enrollment
from services.schedules_service.schedules_repository import find_schedules_by_course
from services.courses_service.courses_repository import find_course_by_id
from services.students_service.students_repository import find_student_by_id
from services.enrollments_service.enrollments_repository import create_enrollment, fetch_enrollments, find_enrollments_by_student, find_enrollments_by_students_all

logger = logging.getLogger(__name__)


def create_enrollment_service(enrollment_data: EnrollmentCreate, db: Session):

    try:
        # Checking Course exists or not
        course = find_course_by_id(
            course_id=enrollment_data.course_id,
            db=db
        )
        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course with this ID don't exists"
            )

        # Checking Course schedule exists or not
        schedules = find_schedules_by_course(
            course_id=enrollment_data.course_id,
            db=db
        )
        if not schedules:
            raise HTTPException(
                status_code=404,
                detail="No Schedule against this course exists"
            )

        # Checking Student exists or not
        student = find_student_by_id(
            student_id=enrollment_data.student_id,
            db=db
        )
        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student with this ID don't exists"
            )

        # Creating a new enrollment instance
        new_enrollment = Enrollment(
            id=uuid4(),
            student_id=UUID(enrollment_data.student_id),
            course_id=UUID(enrollment_data.course_id),
            enrollment_date=enrollment_data.enrollment_date
        )

        # Save the new Enrollment to the database
        saved_enrollment = create_enrollment(new_enrollment, db)

        # Response Obj
        response_data = {
            "student_id": saved_enrollment.student_id,
            "course_id": saved_enrollment.course_id,
            "enrollment_date": saved_enrollment.enrollment_date
        }

        return response_data

    except (Exception, ValueError) as e:
        raise HTTPException(status_code=500, detail=str(e))


def fetch_enrollments_service(limit: int = 10, offset: int = 0, db: Session = None):
    try:
        enrollments = fetch_enrollments(
            limit=limit,
            offset=offset,
            db=db
        )
        return [

            {
                "student_id": enrollment.student_id,
                "course_id": enrollment.course_id,
                "enrollment_date": enrollment.enrollment_date
            }
            for enrollment in enrollments
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )


def fetch_enrollments_by_student_service(student_id: UUID, db: Session, limit: int, offset: int):
    try:
        # First checking student existance
        student = find_student_by_id(
            student_id=str(student_id),
            db=db
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student with this id doesnot exists"
            )

        # Fetching enrollments by student
        enrollments = find_enrollments_by_student(
            student_id=student_id,
            db=db,
            limit=limit,
            offset=offset
        )

        return [

            {
                "student": enrollment.student,
                "course": enrollment.course,
                "enrollment_date": enrollment.enrollment_date
            }
            for enrollment in enrollments
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def fetch_send_enrollments_service(db: Session, user_data: dict):
    try:

        enrollments = find_enrollments_by_students_all(
            db=db
        )

        # Enrollments Object Formation
        enrollments_obj = [
            {
                "id": str(enrollment.id),
                "student_id": str(enrollment.student_id),
                "course_id": str(enrollment.course_id),
                "enrollment_date": str(enrollment.enrollment_date)
            }
            for enrollment in enrollments
        ]

        # Calling api to send enrollments
        response = requests.post(
            url="http://acss_service:8000/api/micro-acss/enrollments/enrollments_recieve/",
            json=enrollments_obj,
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
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
