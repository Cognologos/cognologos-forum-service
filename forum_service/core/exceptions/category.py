from .abc import AbstractException, ConflictException, NotFoundException, UnauthorizedException


class CategoryException(AbstractException):
    """Base Category exception."""


class CategoryNotFoundException(CategoryException, NotFoundException):
    """Category not found."""

    detail = "Category not found"


class CategoryNameAlreadyExistsException(CategoryException, ConflictException):
    """Category name already exists."""

    auto_additional_info_fields = ["name"]

    detail = "Category with name {name} already exists, please use another name"
