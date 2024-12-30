from .abc import AbstractException, ConflictException, NotFoundException


class PostException(AbstractException):
    pass


class PostNotFoundException(PostException, NotFoundException):
    auto_additional_info_fields = ["post_id"]

    detail = "Post {post_id} not found"


class PostNameAlreadyExistsException(PostException, ConflictException):
    """Post name already exists."""

    auto_additional_info_fields = ["name"]

    detail = "Post with name {name} already exists, please use another name"
