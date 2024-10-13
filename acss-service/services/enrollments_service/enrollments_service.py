from typing import List
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Enrollment

from services.enrollments_service.enrollments_response import EnrollmentResponse
from services.enrollments_service.enrollments_repository import create_enrollment, fetch_enrollments, find_enrollment_by_id

logger = logging.getLogger(__name__)


def create_enrollments_recieved(enrollments_data: List[EnrollmentResponse], db: Session):

    try:
        logger.info("Data Persistance Started")
        for enrollment in enrollments_data:
            # Checking for enrollment existance
            enrollment_exists = find_enrollment_by_id(
                enrollment_id=enrollment.id,
                db=db
            )
            if enrollment_exists:
                continue

            # Creation of enrollment
            new_enrollment = Enrollment(
                id=enrollment.id,
                course_id=enrollment.course_id,
                student_id=enrollment.student_id,
                enrollment_date=enrollment.enrollment_date
            )
            create_enrollment(
                enrollment=new_enrollment,
                db=db
            )
        logger.info("enrollments persisted")

        # Fetching the enrollments persisted
        enrollments = fetch_enrollments(db=db)

        enrollments_json = [
            {
                "id": str(enrollment.id),
                "student_id": str(enrollment.student_id),
                "course_id": str(enrollment.course_id),
                "enrollment_date": str(enrollment.enrollment_date)
            }
            for enrollment in enrollments
        ]

        return {
            "status": 200,
            "response": enrollments_json
        }

    except Exception as e:
        logger.error("Error : %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
