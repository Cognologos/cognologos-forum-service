from fastapi import APIRouter

from forum_service.core.dependencies.fastapi import DatabaseDependency
from forum_service.lib.db import category as categories_db
from forum_service.lib.schemas.category import CategoryCreateSchema, CategorySchema


router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategorySchema)
async def create_categories(db: DatabaseDependency, schema: CategoryCreateSchema) -> CategorySchema:
    return await categories_db.create_category(db, schema=schema)
