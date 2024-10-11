from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(),
                        onupdate=datetime.now())


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    program_enrolled = Column(String, nullable=False)

    # Define the relationship to Enrollment
    enrollments = relationship("Enrollment", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)

    # Define the relationship to Enrollment
    enrollments = relationship("Enrollment", back_populates="course")

    # Define the relationship to Schedule
    schedules = relationship("Schedule", back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey(
        "students.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey(
        "courses.id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)

    # Relationships to Student and Course
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey(
        "courses.id"), nullable=False)
    room = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    day_of_week = Column(String, nullable=False)

    # Relationship to Course
    course = relationship("Course", back_populates="schedules")
