from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models import Enrollment


def create_enrollment(enrollment: Enrollment, db: Session):
    db.add(enrollment)
    try:
        db.commit()
        # Refresh to get the newly created enrollment's data from the DB
        db.refresh(enrollment)
        return enrollment
    except Exception as e:
        db.rollback()
        raise e


def fetch_enrollments(db: Session, limit: int = 10, offset: int = 0) -> List[Enrollment]:
    try:
        enrollments = db.query(Enrollment).limit(limit).offset(offset).all()
        return enrollments
    except Exception as e:
        raise e


def find_enrollment_by_id(enrollment_id: UUID, db: Session):
    try:
        enrollment = db.query(Enrollment).filter(
            Enrollment.id == UUID(enrollment_id)).first()
        return enrollment
    except Exception as e:
        raise e


def find_enrollments_by_student(student_id: UUID, db: Session, limit: int = 10, offset: int = 0):
    try:
        from models import Course
        from models import Student

        # Finding enrollments by student_id and joining with courses
        enrollments = (
            db.query(Enrollment)
            .join(Course, Enrollment.course_id == Course.id)
            .join(Student, Enrollment.student_id == Student.id)
            .options(
                joinedload(Enrollment.course),
                joinedload(Enrollment.student)
            )
            .filter(Enrollment.student_id == student_id)
            .limit(limit)
            .offset(offset)
            .all()
        )

        return enrollments

    except Exception as e:
        raise e


def find_enrollments_by_students_all(db: Session):
    try:
        from models import Course
        from models import Student

        # Finding enrollments by student_id and joining with courses
        enrollments = (
            db.query(Enrollment)
            .join(Course, Enrollment.course_id == Course.id)
            .join(Student, Enrollment.student_id == Student.id)
            .all()
        )

        return enrollments

    except Exception as e:
        raise e
