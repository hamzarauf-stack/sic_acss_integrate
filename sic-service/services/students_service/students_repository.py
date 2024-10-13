from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from models import Student


def find_user_by_email(email: str, db: Session):
    return db.query(Student).filter(Student.email == email).first()


def create_student(student: Student, db: Session):
    db.add(student)
    try:
        db.commit()
        # Refresh to get the newly created student's data from the DB
        db.refresh(student)
        return student
    except Exception as e:
        db.rollback()
        raise e


def fetch_students(db: Session, limit: int = 10, offset: int = 0) -> List[Student]:
    students = db.query(Student).limit(limit).offset(offset).all()
    return students


def find_student_by_id(student_id: UUID, db: Session):
    student = db.query(Student).filter(
        Student.id == UUID(student_id)).first()
    return student
