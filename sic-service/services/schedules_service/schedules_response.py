from pydantic import BaseModel
from uuid import UUID


class Course(BaseModel):
    id: UUID
    name: str
    instructor: str
    credits: int


class Room(BaseModel):
    id: UUID
    name: str
    capacity: int


class ScheduleItem(BaseModel):
    id: UUID
    course: Course
    rooms: Room
    start_time: str
    end_time: str
    day_of_week: str
