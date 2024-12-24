from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from forum_service.lib.models.comments import CommentModel
from forum_service.lib.models.posts import PostModel
from forum_service.lib.models.user import UserModel
from forum_service.lib.schemas.comments import CommentCreate, CommentUpdate


# from forum_service.lib.models.comment_reaction import CommentReaction


async def get_post_by_id(post_id: int, session: AsyncSession) -> PostModel:
    return await session.get(PostModel, post_id)


async def get_user_by_id(user_id: int, session: AsyncSession) -> UserModel:
    return await session.get(UserModel, user_id)


async def create_comment_db(
    comment: CommentCreate, author: UserModel, post: PostModel, session: AsyncSession
) -> CommentModel:
    new_comment = CommentModel(content=comment.content, post=post, author=author)
    session.add(new_comment)
    try:
        await session.commit()
        await session.refresh(new_comment)
        return new_comment
    except SQLAlchemyError:
        await session.rollback()
        raise


async def get_comment_by_id(comment_id: int, session: AsyncSession) -> CommentModel:
    return await session.get(CommentModel, comment_id)


async def update_comment_db(comment: CommentUpdate, db_comment: CommentModel, session: AsyncSession) -> CommentModel:
    db_comment.content = comment.content
    session.add(db_comment)
    try:
        await session.commit()
        await session.refresh(db_comment)
        return db_comment
    except SQLAlchemyError:
        await session.rollback()
        raise


async def delete_comment_db(db_comment: CommentModel, session: AsyncSession) -> None:
    try:
        await session.delete(db_comment)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise


async def like_comment_db(comment: CommentModel, session: AsyncSession) -> CommentModel:
    comment.likes += 1
    try:
        await session.commit()
        await session.refresh(comment)
        return comment
    except SQLAlchemyError:
        await session.rollback()
        raise


async def dislike_comment_db(comment: CommentModel, session: AsyncSession) -> CommentModel:
    comment.dislikes += 1
    try:
        await session.commit()
        await session.refresh(comment)
        return comment
    except SQLAlchemyError:
        await session.rollback()
        raise
