from sqlalchemy.orm import Session
from uuid import UUID

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


def fetch_enrollments(db: Session):
    enrollments = db.query(Enrollment).all()
    return enrollments


def find_enrollment_by_id(enrollment_id, db: Session):
    return db.query(Enrollment).filter(
        Enrollment.id == UUID(enrollment_id)).first()
