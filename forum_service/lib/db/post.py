from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.lib.models.post import PostModel
from forum_service.lib.schemas.pagination import PaginationRequest
from forum_service.lib.schemas.post import PostCreateSchema, PostFilterRequest, PostPaginationResponse, PostSchema
from forum_service.lib.utils.filter import add_filters_to_query
from forum_service.lib.utils.pagination import add_pagination_to_query, get_rows_count_in


async def create_post(db: AsyncSession, *, user_id: int, schema: PostCreateSchema) -> PostSchema:
    post_model = PostModel(**schema.model_dump(exclude={"user_id"}), user_id=user_id)
    db.add(post_model)
    await db.flush()
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
