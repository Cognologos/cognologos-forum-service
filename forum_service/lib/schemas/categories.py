from .abc import BaseSchema


class CategoryCreate(BaseSchema):
    name: str
    description: str


class CategoryResponse(BaseSchema):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
