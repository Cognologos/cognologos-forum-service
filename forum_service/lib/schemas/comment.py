from .abc import BaseSchema


class BaseCommentSchema(BaseSchema):
    content: str
    post_id: int


class CommentCreateSchema(BaseCommentSchema):
    pass


class CommentUpdateSchema(BaseSchema):
    content: str


class CommentSchema(CommentCreateSchema):
    id: int
