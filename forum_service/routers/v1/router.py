from fastapi import APIRouter

from . import category, comment, post


router = APIRouter(prefix="/v1")

for i in [
    category.router,
    post.router,
    comment.router,
]:
    router.include_router(i)
