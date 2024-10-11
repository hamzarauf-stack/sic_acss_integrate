from pydantic import BaseModel
from pydantic import field_validator
from uuid import UUID
from datetime import time
from enum import Enum


class ValidWeekDays(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"


class ScheduleCreate(BaseModel):
    course_id: str
    room: str
    start_time: time
    end_time: time
    day_of_week: ValidWeekDays

    @field_validator('start_time', 'end_time')
    def validate_time_format(cls, v):
        # Check if the input is an instance of time
        if not isinstance(v, time):
            raise ValueError(
                'Time must be a valid time object of form 09:00:00')
        return v

    @field_validator('end_time')
    def validate_end_time(cls, end_time, info):
        # Access start_time using info.data which is a dictionary-like object
        start_time = info.data.get('start_time')
        if start_time is not None and end_time <= start_time:
            raise ValueError('end_time must be after start_time')
        return end_time
