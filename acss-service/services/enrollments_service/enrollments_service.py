from typing import List
import logging
from sqlalchemy.orm import Session
from models import Enrollment

from services.enrollments_service.enrollments_response import EnrollmentResponse
from services.enrollments_service.enrollments_repository import create_enrollment

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

        return {
            "status": 200,
            "response": "Data Persisted"
        }

    except Exception as e:
        raise e
