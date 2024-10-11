from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from uuid import UUID
import logging

from services.enrollments_service.enrollment_create import EnrollmentCreate
from db import get_db
from services.enrollments_service.enrollments_service import create_enrollment_service, fetch_enrollments_service, fetch_enrollments_by_student_service, fetch_send_enrollments_service
from auth_dependency.auth_verify import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def get_enrollments(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return fetch_enrollments_service(
        limit=limit,
        offset=offset,
        db=db
    )


@router.post("/")
def create_enrollment(enrollment_data: EnrollmentCreate, db: Session = Depends(get_db)):
    return create_enrollment_service(
        enrollment_data=enrollment_data,
        db=db
    )


@router.get("/{student_id}")
def get_enrollments_by_student(student_id: UUID, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return fetch_enrollments_by_student_service(
        student_id=student_id,
        db=db,
        limit=limit,
        offset=offset
    )


@router.post("/send_enrollments")
def send_enrollments(db: Session = Depends(get_db), user_data: dict = Depends(get_current_user)):
    return fetch_send_enrollments_service(
        db=db,
        user_data=user_data
    )
