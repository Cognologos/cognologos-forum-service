from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from forum_service.lib.models.posts import Post
from forum_service.lib.models.user import User
from forum_service.lib.models.categories import Category
from forum_service.lib.schemas.posts import PostCreate
from forum_service.lib.models.posts import Post
from forum_service.lib.models.posts import PostReaction




async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    return await session.get(User, user_id)


async def get_category_by_id(category_id: int, session: AsyncSession) -> Category:
    return await session.get(Category, category_id)


async def create_post_db(post: PostCreate, author: User, category: Category, session: AsyncSession) -> Post:
    new_post = Post(title=post.title, content=post.content, author=author, category=category)
    session.add(new_post)
    try:
        await session.commit()
        await session.refresh(new_post)
        return new_post
    except SQLAlchemyError:
        await session.rollback()
        raise


async def get_post_by_id_with_relations(post_id: int, session: AsyncSession) -> Post:
    stmt = select(Post).where(Post.id == post_id).options(selectinload(Post.author), selectinload(Post.category))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_post_db(post: PostCreate, db_post: Post, category: Category, session: AsyncSession) -> Post:
    db_post.title = post.title
    db_post.content = post.content
    db_post.category = category
    try:
        await session.commit()
        await session.refresh(db_post)
        return db_post
    except SQLAlchemyError:
        await session.rollback()
        raise


async def delete_post_db(db_post: Post, session: AsyncSession) -> None:
    try:
        await session.delete(db_post)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise


async def like_post_db(post: Post, session: AsyncSession) -> Post:
    post.likes += 1
    try:
        await session.commit()
        await session.refresh(post)
        return post
    except SQLAlchemyError:
        await session.rollback()
        raise


async def dislike_post_db(post: Post, session: AsyncSession) -> Post:
    post.dislikes += 1
    try:
        await session.commit()
        await session.refresh(post)
        return post
    except SQLAlchemyError:
        await session.rollback()
        raise


async def add_or_update_reaction(post_id: int, user_id: int, reaction_type: str, session: AsyncSession) -> dict:
    existing_reaction = await session.execute(
        select(PostReaction).where(PostReaction.post_id == post_id, PostReaction.user_id == user_id)
    )
    existing_reaction = existing_reaction.scalar_one_or_none()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            await session.delete(existing_reaction)
            await session.commit()
            return {"message": f"Reaction {reaction_type} removed"}
        else:
            existing_reaction.reaction_type = reaction_type
            await session.commit()
            await session.refresh(existing_reaction)
            return {"message": f"Reaction updated to {reaction_type}"}
    else:
        new_reaction = PostReaction(post_id=post_id, user_id=user_id, reaction_type=reaction_type)
        session.add(new_reaction)
        await session.commit()
        await session.refresh(new_reaction)
        return {"message": f"Reaction {reaction_type} added"}
