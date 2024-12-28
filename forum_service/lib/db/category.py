from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.lib.models.category import CategoryModel
from forum_service.lib.schemas.category import CategoryCreateSchema, CategorySchema


async def create_category(db: AsyncSession, *, schema: CategoryCreateSchema) -> CategorySchema:
    category_model = CategoryModel(**schema.model_dump())
    db.add(category_model)
    await db.flush()
    return CategorySchema.model_construct(**category_model.to_dict())
