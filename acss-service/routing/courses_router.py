from uuid import UUID
from typing import List
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db
from services.courses_service.courses_create import CourseCreate
from services.courses_service.courses_service import create_course_service, fetch_courses_service, fetch_course_by_id_service


router = APIRouter()


@router.post("/", response_model=CourseCreate)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course_service(course, db)


@router.get("/", response_model=List[CourseCreate])
def fetch_courses(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    courses = fetch_courses_service(db=db, limit=limit, offset=offset)
    return courses


@router.get("/{course_id}", response_model=CourseCreate)
def find_course_by_id(course_id: UUID, db: Session = Depends(get_db)):
    course = fetch_course_by_id_service(course_id=str(course_id), db=db)
    return course
