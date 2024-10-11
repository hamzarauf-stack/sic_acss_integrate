from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    # Relationship to schedules
    schedules = relationship("Schedule", back_populates="rooms")


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)

    # Relationship to enrollments and schedules
    enrollments = relationship("Enrollment", back_populates="courses")
    schedules = relationship("Schedule", back_populates="courses")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    room_id = Column(UUID(as_uuid=True), ForeignKey(
        "rooms.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey(
        "courses.id"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    day_of_week = Column(String, nullable=False)

    # Relationship to Course and Rooms
    rooms = relationship("Room", back_populates="schedules")
    courses = relationship("Course", back_populates="schedules")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    student_id = Column(String, nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey(
        "courses.id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)

    # Relationship to Course
    courses = relationship("Course", back_populates="enrollments")
