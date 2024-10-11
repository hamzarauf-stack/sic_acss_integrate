from sqlalchemy.orm import Session

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
