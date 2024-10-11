from uuid import UUID
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException
from services.students_service.student_create import StudentCreate
from models import Student
from services.students_service.students_repository import find_user_by_email, create_student, fetch_students, find_student_by_id


def create_student_service(student_data: StudentCreate, db: Session):
    try:
        # Check if a student with the given email already exists
        existing_student = find_user_by_email(email=student_data.email, db=db)

        if existing_student:
            raise HTTPException(
                status_code=400, detail="A student with this email already exists"
            )

        # Creating a new student instance
        new_student = Student(
            id=uuid4(),
            name=student_data.name,
            email=student_data.email,
            date_of_birth=student_data.date_of_birth,
            program_enrolled=student_data.program_enrolled,
        )

        # Save the new student to the database
        saved_student = create_student(new_student, db)

        # Response Obj
        response_data = {
            "name": saved_student.name,
            "email": saved_student.email,
            "date_of_birth": saved_student.date_of_birth.strftime("%Y-%m-%d"),
            "program_enrolled": saved_student.program_enrolled,
        }

        return response_data

    except (Exception, ValueError) as e:
        raise HTTPException(status_code=500, detail=str(e))


def fetch_students_service(limit: int = 10, offset: int = 0, db: Session = None):
    try:
        students = fetch_students(
            limit=limit,
            offset=offset,
            db=db
        )
        return [

            {
                "name": student.name,
                "email": student.email,
                "date_of_birth": student.date_of_birth.strftime("%Y-%m-%d"),
                "program_enrolled": student.program_enrolled,
            }
            for student in students
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )


def fetch_student_by_id_service(student_id: UUID, db: Session):
    try:
        student = find_student_by_id(
            student_id=student_id,
            db=db
        )
        if student is None:
            raise HTTPException(
                status_code=404,
                detail="A Student with this id not found"
            )

        # Response Obj
        response_data = {
            "name": student.name,
            "email": student.email,
            "date_of_birth": student.date_of_birth.strftime("%Y-%m-%d"),
            "program_enrolled": student.program_enrolled,
        }

        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
