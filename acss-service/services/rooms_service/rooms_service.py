from uuid import UUID
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException

from services.rooms_service.rooms_create import RoomCreate
from models import Room
from services.rooms_service.rooms_repository import create_room, fetch_rooms, find_room_by_id


def create_room_service(room_data: RoomCreate, db: Session):
    try:
        # Creating a new room instance
        new_room = Room(
            id=uuid4(),
            name=room_data.name,
            capacity=room_data.capacity
        )

        # Save the new room to the database
        saved_room = create_room(new_room, db)

        # Response Obj
        response_data = {
            "name": saved_room.name,
            "capacity": saved_room.capacity
        }

        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def fetch_rooms_service(limit: int = 10, offset: int = 0, db: Session = None):
    try:
        rooms = fetch_rooms(
            limit=limit,
            offset=offset,
            db=db
        )
        return [

            {
                "name": room.name,
                "capacity": room.capacity
            }
            for room in rooms
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )


def fetch_room_by_id_service(room_id: UUID, db: Session):
    try:
        room = find_room_by_id(
            room_id=room_id,
            db=db
        )
        if room is None:
            raise HTTPException(
                status_code=404,
                detail="A Room with this id not found"
            )

        # Response Obj
        response_data = {
            "name": room.name,
            "capacity": room.capacity
        }

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
