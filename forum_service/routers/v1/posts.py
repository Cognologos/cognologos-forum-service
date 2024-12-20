from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from forum_service.core.dependencies.fastapi import db_session
from forum_service.lib.models.posts import Post
from forum_service.lib.models.user import User
from forum_service.lib.models.categories import Category
from forum_service.lib.schemas.posts import PostCreate, PostResponse
from forum_service.lib.schemas.users import UserResponse
from forum_service.lib.schemas.categories import CategoryResponse
from forum_service.lib.db.posts import add_or_update_reaction

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, session: AsyncSession = Depends(db_session)):
    author = await session.get(User, 1)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    category = await session.get(Category, post.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_post = Post(title=post.title, content=post.content, author=author, category=category)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)

    return PostResponse(
        id=new_post.id,
        title=new_post.title,
        content=new_post.content,
        created_at=new_post.created_at,
        author=UserResponse(id=author.id, username=author.username, email=author.email),
        category=CategoryResponse(id=category.id, name=category.name, description=category.description),
    )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post: PostCreate, session: AsyncSession = Depends(db_session)):
    stmt = select(Post).where(Post.id == post_id).options(selectinload(Post.author), selectinload(Post.category))
    result = await session.execute(stmt)
    db_post = result.scalar_one_or_none()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    category_stmt = select(Category).where(Category.id == post.category_id)
    category_result = await session.execute(category_stmt)
    category = category_result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_post.title = post.title
    db_post.content = post.content
    db_post.category = category

    try:
        await session.commit()
        await session.refresh(db_post)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Failed to update post")

    return PostResponse(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        created_at=db_post.created_at,
        author=UserResponse(id=db_post.author.id, username=db_post.author.username, email=db_post.author.email),
        category=CategoryResponse(id=db_post.category.id, name=db_post.category.name,
                                  description=db_post.category.description),
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, session: AsyncSession = Depends(db_session)):
    stmt = select(Post).where(Post.id == post_id)
    result = await session.execute(stmt)
    db_post = result.scalar_one_or_none()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        await session.delete(db_post)
        await session.commit()
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Failed to delete post")

    return None


@router.post("/{post_id}/like")
async def like_post(post_id: int, user_id: int, session: AsyncSession = Depends(db_session)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    response = await add_or_update_reaction(post_id, user_id, "like", session)
    return response


@router.post("/{post_id}/dislike")
async def dislike_post(post_id: int, user_id: int, session: AsyncSession = Depends(db_session)):
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    response = await add_or_update_reaction(post_id, user_id, "dislike", session)
    return response
