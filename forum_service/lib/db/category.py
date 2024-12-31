from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from forum_service.core.exceptions.category import (
    CategoryNameAlreadyExistsException,
    CategoryNotFoundException,
    UserNotAuthorError,
)
from forum_service.lib.models import CategoryModel
from forum_service.lib.schemas.category import CategoryCreateSchema, CategorySchema


async def is_category_exists(db: AsyncSession, name: str) -> bool:
    query = select(CategoryModel).where(CategoryModel.name == name)
    return bool((await db.execute(query)).scalar_one_or_none())


async def raise_for_category_name(db: AsyncSession, name: str) -> None:
    if await is_category_exists(db, name):
        raise CategoryNameAlreadyExistsException(name=name)


async def create_category(db: AsyncSession, *, user_id: int, schema: CategoryCreateSchema) -> CategorySchema:
    await raise_for_category_name(db, schema.name)
    category_model = CategoryModel(**schema.model_dump(exclude={"user_id"}), user_id=user_id)
    db.add(category_model)
    await db.flush()
    return CategorySchema.model_construct(**category_model.to_dict())


async def get_category_model_by_id(
    db: AsyncSession,
    *,
    category_id: int,
) -> CategoryModel:
    query = select(CategoryModel).where(CategoryModel.id == category_id)
    result = (await db.execute(query)).scalar_one_or_none()
    if result is None:
        raise CategoryNotFoundException
    if result.deleted_at is not None:
        raise CategoryNotFoundException
    return result


async def get_category(
    db: AsyncSession,
    *,
    category_id: int,
) -> CategorySchema:
    category_model = await get_category_model_by_id(db, category_id=category_id)
    return CategorySchema.model_construct(**category_model.to_dict())


async def delete_category(
    db: AsyncSession,
    *,
    user_id: int,
    category_id: int,
) -> None:
    category_model = await get_category_model_by_id(db, category_id=category_id)

    if category_model.user_id != user_id:
        raise UserNotAuthorError

    category_model.deleted_at = datetime.now(timezone.utc)

    await db.flush()


async def update_category(
    db: AsyncSession,
    *,
    user_id: int,
    category_id: int,
    schema: CategoryCreateSchema,
) -> CategorySchema:
    category_model = await get_category_model_by_id(db, category_id=category_id)
    if category_model.user_id != user_id:
        raise UserNotAuthorError

    if category_model.name != schema.name:
        await raise_for_category_name(db, schema.name)

    for field, value in schema.model_dump().items():
        setattr(category_model, field, value)

    await db.flush()
    return CategorySchema.model_construct(**category_model.to_dict())
