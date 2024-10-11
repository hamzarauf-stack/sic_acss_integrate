from typing import List
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from db import get_db
from sqlalchemy.orm import Session

from services.students_service.student_create import StudentCreate
from services.students_service.students_service import create_student_service, fetch_students_service, fetch_student_by_id_service


router = APIRouter()


@router.post("/", response_model=StudentCreate)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student_service(student, db)


@router.get("/", response_model=List[StudentCreate])
def fetch_students(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    students = fetch_students_service(db=db, limit=limit, offset=offset)
    return students


@router.get("/{student_id}", response_model=StudentCreate)
def find_student_by_id(student_id: UUID, db: Session = Depends(get_db)):
    student = fetch_student_by_id_service(student_id=str(student_id), db=db)
    return student
