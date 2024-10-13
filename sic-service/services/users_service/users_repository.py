from uuid import UUID
from models import User
from sqlalchemy.orm import Session
from sqlalchemy import or_


def find_user_by_email_or_username(email: str, username: str, db: Session):
    return db.query(User).filter(
        or_(User.email == email, User.username == username)
    ).first()


def find_user_by_id(user_id: UUID, db: Session):

    user = db.query(User).filter(
        User.id == UUID(user_id)).first()
    return user


def create_user(user: User, db: Session):
    db.add(user)
    try:
        db.commit()
        # Refresh to get the newly created users's data from the DB
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e
