from fastapi import APIRouter

from forum_service.core.dependencies.fastapi import DatabaseDependency, UserDependency
from forum_service.lib.db import category as category_db
from forum_service.lib.schemas.category import CategoryCreateSchema, CategorySchema


router = APIRouter(tags=["category"], prefix="/category")


@router.post("/", response_model=CategorySchema)
async def create_category(db: DatabaseDependency, user: UserDependency, schema: CategoryCreateSchema) -> CategorySchema:
    return await category_db.create_category(db, user_id=user.id, schema=schema)


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(db: DatabaseDependency, category_id: int) -> CategorySchema:
    return await category_db.get_category(db, category_id=category_id)


@router.put("/update_category", response_model=CategorySchema)
async def update_category(
    db: DatabaseDependency, user: UserDependency, category_id: int, schema: CategoryCreateSchema
) -> CategorySchema:
    return await category_db.update_category(db, user_id=user.id, category_id=category_id, schema=schema)


@router.delete("/delete_category", status_code=204)
async def delete_category(db: DatabaseDependency, user: UserDependency, category_id: int) -> None:
    return await category_db.delete_category(db, user_id=user.id, category_id=category_id)
