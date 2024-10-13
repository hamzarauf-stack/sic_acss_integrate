from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import uuid4
from datetime import timedelta

from models import User
from services.users_service.users_repository import find_user_by_email_or_username, create_user
from services.users_service.user_create import UserCreate, UserLogin

from utilities.bcrypt_utility import get_password_hash, verify_password
from utilities.jwt_utility import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


def create_user_service(user_data: UserCreate, db: Session):
    try:
        # Check if a user with the given email already exists
        existing_student = find_user_by_email_or_username(
            email=user_data.email,
            username=user_data.username,
            db=db
        )

        if existing_student:
            raise HTTPException(
                status_code=400, detail="A user with this email or username already exists"
            )

        user_data.hashed_password = get_password_hash(
            password=user_data.hashed_password
        )

        # Creating a new user instance
        new_user = User(
            id=uuid4(),
            username=user_data.username,
            email=user_data.email,
            hashed_password=user_data.hashed_password
        )

        # Save the new student to the database
        saved_user = create_user(new_user, db)

        # Response Obj
        response_data = {
            "username": saved_user.username,
            "email": saved_user.email
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def login_user_service(user_data: UserLogin, db: Session):
    try:
        user = find_user_by_email_or_username(
            email=user_data.username,
            username=user_data.username,
            db=db
        )
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Generate token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "can_access": True}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
