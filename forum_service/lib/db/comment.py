from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from forum_service.lib.models.comment import CommentModel
from forum_service.lib.schemas.comment import CommentCreateSchema, CommentSchema
from forum_service.core.exceptions.comment import CommentNotFoundException


async def create_comment(db: AsyncSession, *, user_id: int, schema: CommentCreateSchema) -> CommentSchema:
    comment_model = CommentModel(**schema.model_dump(exclude={"user_id"}), user_id=user_id)
    db.add(comment_model)
    await db.flush()
    return CommentSchema.model_construct(**comment_model.to_dict())


async def get_comment_model_by_id(
        db: AsyncSession,
        *,
        comment_id: int,
) -> CommentModel:
    query = select(CommentModel).where(CommentModel.id == comment_id)
    result = (await db.execute(query)).scalar_one_or_none()
    if result is None:
        raise CommentNotFoundException
    if result.deleted_at is not None:
        raise CommentNotFoundException
    return result


async def get_comment(
        db: AsyncSession,
        *,
        comment_id: int,
) -> CommentSchema:
    comment_model = await get_comment_model_by_id(db, comment_id=comment_id)
    return CommentSchema.model_construct(**comment_model.to_dict())


async def delete_comment(
        db: AsyncSession,
        *,
        comment_id: int,
) -> None:
    comment_model = await get_comment_model_by_id(db, comment_id=comment_id)
    comment_model.deleted_at = datetime.now(timezone.utc)

    await db.flush()


async def update_comment(
        db: AsyncSession,
        *,
        comment_id: int,
        schema: CommentCreateSchema,
) -> CommentSchema:
    comment_model = await get_comment_model_by_id(db, comment_id=comment_id)

    for field, value in schema.model_dump().items():
        setattr(comment_model, field, value)

    await db.flush()
    return CommentSchema.model_construct(**comment_model.to_dict())
