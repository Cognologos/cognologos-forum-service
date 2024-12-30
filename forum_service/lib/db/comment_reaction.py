from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.core.exceptions.comment import CommentNotFoundException
from forum_service.lib.models.comment import CommentModel
from forum_service.lib.models.comment_reaction import CommentReactionModel


async def set_comment_reaction(db: AsyncSession, *, user_id: int, comment_id: int, reaction_type: str) -> None:
    if reaction_type not in {"like", "dislike"}:
        raise ValueError("Invalid reaction type. Must be 'like' or 'dislike'.")

    comment_query = select(CommentModel).where(CommentModel.id == comment_id)
    comment = (await db.execute(comment_query)).scalar_one_or_none()
    if comment is None or comment.deleted_at is not None:
        raise CommentNotFoundException

    reaction_query = select(CommentReactionModel).where(
        (CommentReactionModel.comment_id == comment_id) & (CommentReactionModel.user_id == user_id)
    )
    existing_reaction = (await db.execute(reaction_query)).scalar_one_or_none()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            return
        else:
            existing_reaction.reaction_type = reaction_type
            db.add(existing_reaction)
    else:
        new_reaction = CommentReactionModel(user_id=user_id, comment_id=comment_id, reaction_type=reaction_type)
        db.add(new_reaction)

    await db.flush()
