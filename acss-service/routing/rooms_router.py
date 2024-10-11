from typing import List
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from services.rooms_service.rooms_create import RoomCreate
from services.rooms_service.rooms_service import create_room_service, fetch_rooms_service, fetch_room_by_id_service
from db import get_db

router = APIRouter()


@router.post("/", response_model=RoomCreate)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return create_room_service(room, db)


@router.get("/", response_model=List[RoomCreate])
def fetch_courses(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    rooms = fetch_rooms_service(db=db, limit=limit, offset=offset)
    return rooms


@router.get("/{room_id}", response_model=RoomCreate)
def find_course_by_id(room_id: UUID, db: Session = Depends(get_db)):
    room = fetch_room_by_id_service(room_id=str(room_id), db=db)
    return room
