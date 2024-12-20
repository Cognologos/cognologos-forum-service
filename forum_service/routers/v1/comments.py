from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.core.dependencies.fastapi import db_session
from forum_service.lib.schemas.comments import CommentCreate, CommentUpdate
from forum_service.lib.db.comments import (
    get_post_by_id,
    get_user_by_id,
    create_comment_db,
    get_comment_by_id,
    update_comment_db,
    delete_comment_db,
    like_comment_db,
    dislike_comment_db,
)
# from forum_service.lib.db.comments import add_or_update_reaction
# from forum_service.lib.models.comments import Comment


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, session: AsyncSession = Depends(db_session)):
    post = await get_post_by_id(comment.post_id, session)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    author = await get_user_by_id(1, session)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    try:
        new_comment = await create_comment_db(comment, author, post, session)
        return {"message": "Comment created successfully", "comment": new_comment}
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to create comment")


@router.put("/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    session: AsyncSession = Depends(db_session),
):
    db_comment = await get_comment_by_id(comment_id, session)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    try:
        updated_comment = await update_comment_db(comment, db_comment, session)
        return {"message": "Comment updated successfully", "comment": updated_comment}
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to update comment")


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, session: AsyncSession = Depends(db_session)):
    db_comment = await get_comment_by_id(comment_id, session)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    try:
        await delete_comment_db(db_comment, session)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to delete comment")

    return {"message": "Comment deleted successfully"}


# @router.post("/{comment_id}/like")
# async def like_comment(comment_id: int, session: AsyncSession = Depends(db_session)):
#     comment = await get_comment_by_id(comment_id, session)
#     if not comment:
#         raise HTTPException(status_code=404, detail="Comment not found")
#
#     try:
#         updated_comment = await like_comment_db(comment, session)
#         return {
#             "message": "Comment liked successfully",
#             "likes": updated_comment.likes,
#             "dislikes": updated_comment.dislikes,
#         }
#     except Exception:
#         raise HTTPException(status_code=400, detail="Failed to like comment")
#
#
# @router.post("/{comment_id}/dislike")
# async def dislike_comment(comment_id: int, session: AsyncSession = Depends(db_session)):
#     comment = await get_comment_by_id(comment_id, session)
#     if not comment:
#         raise HTTPException(status_code=404, detail="Comment not found")
#
#     try:
#         updated_comment = await dislike_comment_db(comment, session)
#         return {
#             "message": "Comment disliked successfully",
#             "likes": updated_comment.likes,
#             "dislikes": updated_comment.dislikes,
#         }
#     except Exception:
#         raise HTTPException(status_code=400, detail="Failed to dislike comment")


# @router.post("/{comment_id}/like")
# async def like_post(comment_id: int, user_id: int, session: AsyncSession = Depends(db_session)):
#     comment = await session.get(Comment, comment_id)
#     if not comment:
#         raise HTTPException(status_code=404, detail="Post not found")
#
#     response = await add_or_update_reaction(comment_id, user_id, "like", session)
#     return response
#
#
# @router.post("/{comment_id}/dislike")
# async def dislike_post(comment_id: int, user_id: int, session: AsyncSession = Depends(db_session)):
#     comment = await session.get(Comment, comment_id)
#     if not comment:
#         raise HTTPException(status_code=404, detail="Post not found")
#
#     response = await add_or_update_reaction(comment_id, user_id, "dislike", session)
#     return response
