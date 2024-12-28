from datetime import datetime
from typing import Sequence

from . import fields as f
from .abc import BaseSchema
from .category import CATEGORY_ID
from .enums.filter import FilterType, OrderByType
from .pagination import PaginationResponse
from .user import USER_ID


POST_ID = f.ID(prefix="Post ID.")
POST_TITLE = f.BaseField(description="Post title.", min_length=1, max_length=64, postples=["How do I do that?"])
POST_CONTENT = f.BaseField(description="Post content.", min_length=1, max_length=128, postples=["Example content"])
POST_CREATED_AT = f.DATETIME(prefix="Post creation datetime.")


class PostCreateSchema(BaseSchema):
    title: str = POST_TITLE
    content: str = POST_CONTENT
    category_id: int = CATEGORY_ID


class PostSchema(PostCreateSchema):
    id: int = POST_ID
    user_id: int = USER_ID
    created_at: datetime = POST_CREATED_AT


class PostFilterRequest(BaseSchema):
    post_title_eq: str | None = POST_TITLE(default=None, filter_type=FilterType.eq, table_column="title")
    post_title_ilike: str | None = POST_TITLE(default=None, filter_type=FilterType.ilike, table_column="title")

    category_id_eq: int | None = CATEGORY_ID(default=None, filter_type=FilterType.eq, table_column="category_id")

    created_at_order_by: OrderByType | None = f.ORDER_BY_FILTER(table_column="created_at")

    created_at_from: datetime | None = POST_CREATED_AT(
        default=None, filter_type=FilterType.ge, table_column="created_at"
    )
    created_at_to: datetime | None = POST_CREATED_AT(default=None, filter_type=FilterType.le, table_column="created_at")


class PostPaginationResponse(PaginationResponse[PostSchema]):
    items: Sequence[PostSchema]
