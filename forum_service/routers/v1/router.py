from fastapi import APIRouter
from . import user, posts, comments, categories

router = APIRouter(prefix="/v1")

for i in [
    user.router,
    categories.router,
    posts.router,
    comments.router,
]:
    router.include_router(i)
