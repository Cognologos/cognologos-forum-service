from datetime import datetime

from .abc import BaseSchema


class PostCreateSchema(BaseSchema):
    title: str
    content: str
    category_id: int


class PostSchema(PostCreateSchema):
    id: int
    user_id: int
    created_at: datetime
