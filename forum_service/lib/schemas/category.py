from datetime import datetime
from . import fields as f
from .abc import BaseSchema
from .user import USER_ID


CATEGORY_ID = f.ID(prefix="Category ID.")
CATEGORY_NAME = f.BaseField(description="Category name.", min_length=1, max_length=64, postples=["Maths"])
CATEGORY_DESCRIPTION = f.BaseField(
    description="Category description.", min_length=1, max_length=64, postples=["Maths is when pipec"]
)
CATEGORY_CREATED_AT = f.DATETIME(prefix="Category creation datetime.")


class BaseCategorySchema(BaseSchema):
    name: str = CATEGORY_NAME
    description: str = CATEGORY_DESCRIPTION


class CategoryCreateSchema(BaseCategorySchema):
    pass


class CategorySchema(BaseCategorySchema):
    id: int = CATEGORY_ID
    user_id: int = USER_ID
    created_at: datetime = CATEGORY_CREATED_AT
