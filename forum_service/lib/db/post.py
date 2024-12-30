from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.core.exceptions.post import PostNotFoundException
from forum_service.lib.models.post import PostModel
from forum_service.lib.schemas.pagination import PaginationRequest
from forum_service.lib.schemas.post import PostCreateSchema, PostFilterRequest, PostPaginationResponse, PostSchema
from forum_service.lib.utils.filter import add_filters_to_query
from forum_service.lib.utils.pagination import add_pagination_to_query, get_rows_count_in


async def get_post_model_by_id(
    db: AsyncSession,
    *,
    post_id: int,
) -> PostModel:
    query = select(PostModel).where(PostModel.id == post_id)
    result = (await db.execute(query)).scalar_one_or_none()
    if result is None:
        raise PostNotFoundException
    if result.deleted_at is not None:
        raise PostNotFoundException
    return result


async def get_post(db: AsyncSession, post_id: int) -> PostSchema:
    post_model = await get_post_model_by_id(db, post_id=post_id)
    return PostSchema.model_construct(**post_model.to_dict())


async def get_posts(
    db: AsyncSession, pagination: PaginationRequest, filters: PostFilterRequest
) -> PostPaginationResponse:
    query = select(PostModel)
    query_count = select(func.count(PostModel.id))

    query = add_filters_to_query(query, PostModel, filters)
    query_count = add_filters_to_query(query_count, PostModel, filters, include_order_by=False)
    query = add_pagination_to_query(query, pagination)

    problems = (await db.execute(query)).scalars().all()
    total_items, pages = await get_rows_count_in(db, query_count, pagination.limit)

    items = [PostSchema.model_construct(**problem.to_dict()) for problem in problems]
    return PostPaginationResponse.model_construct(total_items=total_items, total_pages=pages, items=items)


async def create_post(db: AsyncSession, *, user_id: int, schema: PostCreateSchema) -> PostSchema:
    post_model = PostModel(**schema.model_dump(exclude={"user_id"}), user_id=user_id)
    db.add(post_model)
    await db.flush()
    return PostSchema.model_construct(**post_model.to_dict())


async def update_post(
    db: AsyncSession,
    *,
    post_id: int,
    schema: PostCreateSchema,
) -> PostSchema:
    post_model = await get_post_model_by_id(db, post_id=post_id)

    for field, value in schema.model_dump().items():
        setattr(post_model, field, value)

    await db.flush()
    return PostSchema.model_construct(**post_model.to_dict())


async def delete_post(
    db: AsyncSession,
    *,
    post_id: int,
) -> None:
    post_model = await get_post_model_by_id(db, post_id=post_id)
    post_model.deleted_at = datetime.now(timezone.utc)

    await db.flush()
