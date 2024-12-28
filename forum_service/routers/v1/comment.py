from fastapi import APIRouter

from forum_service.core.dependencies.fastapi import DatabaseDependency, UserDependency
from forum_service.lib.db import comment as comments_db
from forum_service.lib.schemas.comment import CommentCreateSchema, CommentSchema


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentSchema)
async def create_comment(db: DatabaseDependency, user: UserDependency, schema: CommentCreateSchema) -> CommentSchema:
    return await comments_db.create_comment(db, user_id=user.id, schema=schema)
