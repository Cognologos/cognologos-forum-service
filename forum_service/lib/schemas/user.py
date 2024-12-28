from datetime import datetime

from . import fields as f
from .abc import BaseSchema


USER_ID = f.ID(prefix="User ID.")


class UserSchema(BaseSchema):
    id: int = USER_ID
    username: str
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
