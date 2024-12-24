from datetime import datetime

from .abc import BaseSchema


class UserSchema(BaseSchema):
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
