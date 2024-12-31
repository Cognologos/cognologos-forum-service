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


class UserNotAuthorError(CommentException, ConflictException):
    """User is not the author of the comment."""

    detail = "You are not the author of this comment"
