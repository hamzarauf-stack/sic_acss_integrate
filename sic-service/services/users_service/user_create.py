from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str


class UserLogin(BaseModel):
    username: str
    password: str
