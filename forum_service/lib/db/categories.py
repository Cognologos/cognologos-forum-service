from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from forum_service.lib.models.categories import Category
from forum_service.lib.schemas.categories import CategoryCreate


async def create_category_db(category: CategoryCreate, session: AsyncSession) -> Category:
    new_category = Category(name=category.name, description=category.description)
    session.add(new_category)
    try:
        await session.commit()
        await session.refresh(new_category)
        return new_category
    except SQLAlchemyError:
        await session.rollback()
        raise


async def update_category_db(category_id: int, category: CategoryCreate, session: AsyncSession) -> Category:
    db_category = await session.get(Category, category_id)
    if not db_category:
        return None

    db_category.name = category.name
    db_category.description = category.description
    try:
        await session.commit()
        await session.refresh(db_category)
        return db_category
    except SQLAlchemyError:
        await session.rollback()
        raise


async def delete_category_db(category_id: int, session: AsyncSession) -> bool:
    db_category = await session.get(Category, category_id)
    if not db_category:
        return False

    try:
        await session.delete(db_category)
        await session.commit()
        return True
    except SQLAlchemyError:
        await session.rollback()
        raise
