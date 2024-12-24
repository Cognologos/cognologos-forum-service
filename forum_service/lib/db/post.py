from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from forum_service.lib.models.categories import CategoryModel
from forum_service.lib.models.posts import PostModel, PostReactionModel
from forum_service.lib.models.user import UserModel
from forum_service.lib.schemas.posts import PostCreate


async def get_user_by_id(user_id: int, session: AsyncSession) -> UserModel:
    return await session.get(UserModel, user_id)


async def get_category_by_id(category_id: int, session: AsyncSession) -> CategoryModel:
    return await session.get(CategoryModel, category_id)


async def create_post_db(
    post: PostCreate, author: UserModel, category: CategoryModel, session: AsyncSession
) -> PostModel:
    new_post = PostModel(title=post.title, content=post.content, author=author, category=category)
    session.add(new_post)
    try:
        await session.commit()
        await session.refresh(new_post)
        return new_post
    except SQLAlchemyError:
        await session.rollback()
        raise


async def get_post_by_id_with_relations(post_id: int, session: AsyncSession) -> PostModel:
    stmt = (
        select(PostModel)
        .where(PostModel.id == post_id)
        .options(selectinload(PostModel.author), selectinload(PostModel.category))
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_post_db(
    post: PostCreate, db_post: PostModel, category: CategoryModel, session: AsyncSession
) -> PostModel:
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


async def delete_post_db(db_post: PostModel, session: AsyncSession) -> None:
    try:
        await session.delete(db_post)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise


async def like_post_db(post: PostModel, session: AsyncSession) -> PostModel:
    post.likes += 1
    try:
        await session.commit()
        await session.refresh(post)
        return post
    except SQLAlchemyError:
        await session.rollback()
        raise


async def dislike_post_db(post: PostModel, session: AsyncSession) -> PostModel:
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
        select(PostReactionModel).where(PostReactionModel.post_id == post_id, PostReactionModel.user_id == user_id)
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
        new_reaction = PostReactionModel(post_id=post_id, user_id=user_id, reaction_type=reaction_type)
        session.add(new_reaction)
        await session.commit()
        await session.refresh(new_reaction)
        return {"message": f"Reaction {reaction_type} added"}
