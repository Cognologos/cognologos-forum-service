from .abc import AbstractException, NotFoundException


class PostException(AbstractException):
    pass


class PostNotFoundException(PostException, NotFoundException):
    auto_additional_info_fields = ["post_id"]

    detail = "Post {post_id} not found"
