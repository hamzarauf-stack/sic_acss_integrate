from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from models import Room


def create_room(room: Room, db: Session):
    db.add(room)
    try:
        db.commit()
        # Refresh to get the newly created room's data from the DB
        db.refresh(room)
        return room
    except Exception as e:
        db.rollback()
        raise e


def fetch_rooms(db: Session, limit: int = 10, offset: int = 0) -> List[Room]:
    rooms = db.query(Room).limit(limit).offset(offset).all()
    return rooms


def find_room_by_id(room_id: UUID, db: Session):
    room = db.query(Room).filter(
        Room.id == UUID(room_id)).first()
    return room
