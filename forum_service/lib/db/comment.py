from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.lib.models.comment import CommentModel
from forum_service.lib.schemas.comment import CommentCreateSchema, CommentSchema


async def create_comment(db: AsyncSession, *, user_id: int, schema: CommentCreateSchema) -> CommentSchema:
    comment_model = CommentModel(**schema.model_dump(exclude={"user_id"}), user_id=user_id)
    db.add(comment_model)
    await db.flush()
    return CommentSchema.model_construct(**comment_model.to_dict())
