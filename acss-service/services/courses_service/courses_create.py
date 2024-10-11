from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    instructor: str
    credits: int
