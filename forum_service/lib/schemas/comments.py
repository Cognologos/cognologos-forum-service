from .abc import BaseSchema


class CommentCreate(BaseSchema):
    content: str
    post_id: int


class CommentUpdate(BaseSchema):
    content: str
