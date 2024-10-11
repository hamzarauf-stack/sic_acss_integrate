from pydantic import BaseModel
from pydantic import field_validator

from datetime import date


class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: str
    enrollment_date: date

    @field_validator('enrollment_date')
    def validate_enrollment_date_format(cls, value):
        # If value is not already a date object, a ValueError will be raised by Pydantic.
        if not isinstance(value, date):
            raise ValueError(
                'Enrollment date must be provided in the format YYYY-MM-DD')
        return value
