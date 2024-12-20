from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.core.dependencies.fastapi import db_session
from forum_service.lib.models.categories import Category
from forum_service.lib.schemas.categories import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(db_session)):
    new_category = Category(name=category.name, description=category.description)
    session.add(new_category)
    try:
        await session.commit()
        await session.refresh(new_category)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
    return new_category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryCreate, session: AsyncSession = Depends(db_session)):
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.name = category.name
    db_category.description = category.description
    try:
        await session.commit()
        await session.refresh(db_category)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Failed to update category")
    return db_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, session: AsyncSession = Depends(db_session)):
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    try:
        await session.delete(db_category)
        await session.commit()
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Failed to delete category")
    return {"detail": "Category deleted successfully"}
