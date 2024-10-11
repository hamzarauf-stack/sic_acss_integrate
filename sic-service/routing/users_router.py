from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from sqlalchemy.orm import Session

from db import get_db
from services.users_service.users_service import create_user_service, login_user_service
from auth_dependency.auth_verify import get_current_user
from services.users_service.user_create import UserCreate, UserLogin

router = APIRouter()


@router.get("/")
def get_users(payload: dict = Depends(get_current_user)):
    return {"message": "Get all users", "payload": payload}


@router.post("/signup")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(
        user_data=user_data,
        db=db
    )


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return login_user_service(
        user_data=user_data,
        db=db
    )
