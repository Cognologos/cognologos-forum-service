from fastapi import APIRouter

from forum_service.core.dependencies.fastapi import DatabaseDependency
from forum_service.lib.db import category as category_db
from forum_service.lib.schemas.category import CategoryCreateSchema, CategorySchema


router = APIRouter(tags=["category"], prefix="/category")


@router.post("/", response_model=CategorySchema)
async def create_category(db: DatabaseDependency, schema: CategoryCreateSchema) -> CategorySchema:
    return await category_db.create_category(db, schema=schema)


@router.get("/get_category", response_model=CategorySchema)
async def get_category(db: DatabaseDependency, category_id: int) -> CategorySchema:
    return await category_db.get_category(db, category_id=category_id)


@router.delete("/get_category", status_code=204)
async def delete_category(db: DatabaseDependency, category_id: int) -> None:
    return await category_db.delete_category(db, category_id=category_id)