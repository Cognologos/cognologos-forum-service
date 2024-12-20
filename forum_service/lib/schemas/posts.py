from .abc import BaseSchema
from forum_service.lib.schemas.users import UserResponse
from forum_service.lib.schemas.categories import CategoryResponse
from datetime import datetime


class PostCreate(BaseSchema):
    title: str
    content: str
    category_id: int


class PostResponse(BaseSchema):
    id: int
    title: str
    content: str
    created_at: datetime
    author: UserResponse
    category: CategoryResponse

    class Config:
        from_attributes = True
