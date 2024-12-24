from .abc import BaseSchema


class BaseCategorySchema(BaseSchema):
    name: str
    description: str


class CategoryCreateSchema(BaseCategorySchema):
    pass


class CategorySchema(BaseCategorySchema):
    id: int
