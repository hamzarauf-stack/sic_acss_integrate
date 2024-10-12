from typing import List
import logging
from sqlalchemy.orm import Session
from models import Enrollment

from services.enrollments_service.enrollments_response import EnrollmentResponse
from services.enrollments_service.enrollments_repository import create_enrollment, fetch_enrollments

logger = logging.getLogger(__name__)


def create_enrollments_recieved(enrollments_data: List[EnrollmentResponse], db: Session):

    try:
        logger.info("Data Persistance Started")
        for enrollment in enrollments_data:
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
        raise e
