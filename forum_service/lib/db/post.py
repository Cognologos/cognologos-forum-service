from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.lib.models.post import PostModel
from forum_service.lib.schemas.post import PostCreateSchema, PostSchema


async def create_post(db: AsyncSession, *, user_id: int, schema: PostCreateSchema) -> PostSchema:
    post_model = PostModel(**schema.model_dump(exclude={"user_id"}), user_id=user_id)
    db.add(post_model)
    await db.flush()
    return PostSchema.model_construct(**post_model.to_dict())
