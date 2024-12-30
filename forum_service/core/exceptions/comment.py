from .abc import AbstractException, ConflictException, NotFoundException, UnauthorizedException


class CommentException(AbstractException):
    """Base Comment exception."""


class CommentNotFoundException(CommentException, NotFoundException):
    """Comment not found."""

    detail = "Comment not found"


class CommentNameAlreadyExistsException(CommentException, ConflictException):
    """Comment name already exists."""

    auto_additional_info_fields = ["name"]

    detail = "Comment with name {name} already exists, please use another name"
