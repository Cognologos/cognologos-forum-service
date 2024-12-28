from .abc import AbstractException, ConflictException


class FilterException(AbstractException):
    pass


class FilterGroupAlreadyInUseException(FilterException, ConflictException):
    detail = "Cannot use the same filter from the same group ({group}) more than once"
