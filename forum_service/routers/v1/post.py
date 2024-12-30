from fastapi import APIRouter
from pyfa_converter_v2 import QueryDepends

from forum_service.core.dependencies.fastapi import DatabaseDependency, UserDependency
from forum_service.lib.db import post as posts_db
from forum_service.lib.schemas.pagination import PaginationRequest
from forum_service.lib.schemas.post import PostCreateSchema, PostFilterRequest, PostPaginationResponse, PostSchema


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostSchema)
async def create_post(db: DatabaseDependency, user: UserDependency, schema: PostCreateSchema) -> PostSchema:
    return await posts_db.create_post(db, user_id=user.id, schema=schema)


@router.get("/", response_model=PostPaginationResponse)
async def get_posts(
    db: DatabaseDependency,
    pagination: PaginationRequest = QueryDepends(PaginationRequest),
    filter: PostFilterRequest = QueryDepends(PostFilterRequest),
) -> PostPaginationResponse:
    return await posts_db.get_posts(db, pagination, filter)


@router.get("/{post_id}", response_model=PostSchema)
async def get_post(db: DatabaseDependency, post_id: int) -> PostSchema:
    return await posts_db.get_post(db, post_id)


@router.put("/update_post", response_model=PostSchema)
async def update_post(db: DatabaseDependency, post_id: int, schema: PostCreateSchema) -> PostSchema:
    return await posts_db.update_post(db, post_id=post_id, schema=schema)


@router.delete("/delete_post", status_code=204)
async def delete_post(db: DatabaseDependency, post_id: int) -> None:
    return await posts_db.delete_post(db, post_id=post_id)
