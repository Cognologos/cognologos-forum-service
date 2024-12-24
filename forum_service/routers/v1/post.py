from fastapi import APIRouter

from forum_service.core.dependencies.fastapi import DatabaseDependency, UserDependency
from forum_service.lib.db import post as post_db
from forum_service.lib.schemas.post import PostCreateSchema, PostSchema


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostSchema)
async def create_post(db: DatabaseDependency, user: UserDependency, schema: PostCreateSchema) -> PostSchema:
    return await post_db.create_post(db, user_id=user.id, schema=schema)
