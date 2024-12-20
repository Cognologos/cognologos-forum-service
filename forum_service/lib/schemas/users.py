from pydantic import EmailStr

from .abc import BaseSchema


class UserCreate(BaseSchema):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseSchema):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
