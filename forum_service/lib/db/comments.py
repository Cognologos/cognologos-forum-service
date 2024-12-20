from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from forum_service.lib.models.posts import Post
from forum_service.lib.models.user import User
from forum_service.lib.schemas.comments import CommentCreate, CommentUpdate
from forum_service.lib.models.comments import Comment
# from forum_service.lib.models.comment_reaction import CommentReaction



async def get_post_by_id(post_id: int, session: AsyncSession) -> Post:
    return await session.get(Post, post_id)


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    return await session.get(User, user_id)


async def create_comment_db(comment: CommentCreate, author: User, post: Post, session: AsyncSession) -> Comment:
    new_comment = Comment(content=comment.content, post=post, author=author)
    session.add(new_comment)
    try:
        await session.commit()
        await session.refresh(new_comment)
        return new_comment
    except SQLAlchemyError:
        await session.rollback()
        raise


async def get_comment_by_id(comment_id: int, session: AsyncSession) -> Comment:
    return await session.get(Comment, comment_id)


async def update_comment_db(comment: CommentUpdate, db_comment: Comment, session: AsyncSession) -> Comment:
    db_comment.content = comment.content
    session.add(db_comment)
    try:
        await session.commit()
        await session.refresh(db_comment)
        return db_comment
    except SQLAlchemyError:
        await session.rollback()
        raise


async def delete_comment_db(db_comment: Comment, session: AsyncSession) -> None:
    try:
        await session.delete(db_comment)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise


async def like_comment_db(comment: Comment, session: AsyncSession) -> Comment:
    comment.likes += 1
    try:
        await session.commit()
        await session.refresh(comment)
        return comment
    except SQLAlchemyError:
        await session.rollback()
        raise


async def dislike_comment_db(comment: Comment, session: AsyncSession) -> Comment:
    comment.dislikes += 1
    try:
        await session.commit()
        await session.refresh(comment)
        return comment
    except SQLAlchemyError:
        await session.rollback()
        raise



# async def add_or_update_reaction(comment_id: int, user_id: int, reaction_type: str, session: AsyncSession) -> dict:
#     existing_reaction = await session.execute(
#         select(CommentReaction).where(CommentReaction.post_id == comment_id, CommentReaction.user_id == user_id)
#     )
#     existing_reaction = existing_reaction.scalar_one_or_none()
#
#     if existing_reaction:
#         if existing_reaction.reaction_type == reaction_type:
#             await session.delete(existing_reaction)
#             await session.commit()
#             return {"message": f"Reaction {reaction_type} removed"}
#         else:
#             existing_reaction.reaction_type = reaction_type
#             await session.commit()
#             await session.refresh(existing_reaction)
#             return {"message": f"Reaction updated to {reaction_type}"}
#     else:
#         new_reaction = CommentReaction(post_id=comment_id, user_id=user_id, reaction_type=reaction_type)
#         session.add(new_reaction)
#         await session.commit()
#         await session.refresh(new_reaction)
#         return {"message": f"Reaction {reaction_type} added"}