from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator
from datetime import datetime
from enum import Enum


class ValidProgramsEnum(str, Enum):
    COMPUTER_SCIENCE = "Computer Science"
    MATHEMATICS = "Mathematics"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    BIOLOGY = "Biology"
    ENGINEERING = "Engineering"


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: str
    program_enrolled: ValidProgramsEnum

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        try:
            # Attempt to parse the date to check if it matches the expected format
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date_of_birth must be in the format yyyy-mm-dd")
        return value
