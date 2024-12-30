from fastapi import APIRouter

from forum_service.core.dependencies.fastapi import DatabaseDependency, UserDependency
from forum_service.lib.db import comment as comments_db
from forum_service.lib.db.comment_reaction import set_comment_reaction as db_set_comment_reaction
from forum_service.lib.schemas.comment import CommentCreateSchema, CommentSchema


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentSchema)
async def create_comment(db: DatabaseDependency, user: UserDependency, schema: CommentCreateSchema) -> CommentSchema:
    return await comments_db.create_comment(db, user_id=user.id, schema=schema)


@router.get("/{comment_id}", response_model=CommentSchema)
async def get_comment(db: DatabaseDependency, comment_id: int) -> CommentSchema:
    return await comments_db.get_comment(db, comment_id=comment_id)


@router.put("/update_comment", response_model=CommentSchema)
async def update_comment(db: DatabaseDependency, comment_id: int, schema: CommentCreateSchema) -> CommentSchema:
    return await comments_db.update_comment(db, comment_id=comment_id, schema=schema)


@router.delete("/delete_comment", status_code=204)
async def delete_comment(db: DatabaseDependency, comment_id: int) -> None:
    return await comments_db.delete_comment(db, comment_id=comment_id)


@router.post("/{comment_id}/like", status_code=204)
async def like_comment(db: DatabaseDependency, user: UserDependency, comment_id: int) -> None:
    await db_set_comment_reaction(db, user_id=user.id, comment_id=comment_id, reaction_type="like")


@router.post("/{comment_id}/dislike", status_code=204)
async def dislike_comment(db: DatabaseDependency, user: UserDependency, comment_id: int) -> None:
    await db_set_comment_reaction(db, user_id=user.id, comment_id=comment_id, reaction_type="dislike")
