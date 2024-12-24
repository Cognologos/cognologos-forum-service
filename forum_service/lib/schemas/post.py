from datetime import datetime

from .abc import BaseSchema


class PostCreateSchema(BaseSchema):
    title: str
    content: str
    user_id: int
    category_id: int


class PostSchema(PostCreateSchema):
    id: int
    created_at: datetime
