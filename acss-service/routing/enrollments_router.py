from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from services.enrollments_service.enrollments_response import EnrollmentResponse
from services.enrollments_service.enrollments_service import create_enrollments_recieved
from auth_dependency.auth_verify import get_current_user

router = APIRouter()


@router.post("/enrollments_recieve")
def fetch_enrollments(enrollments_data: List[EnrollmentResponse], db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_enrollments_recieved(
        enrollments_data=enrollments_data,
        db=db
    )
