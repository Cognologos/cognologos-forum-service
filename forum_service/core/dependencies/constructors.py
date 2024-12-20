from typing import Any, AsyncGenerator, Generator

from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from forum_service.core.config import AppConfig


def db_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(database_url, isolation_level="SERIALIZABLE")


def db_session_maker(
    engine: AsyncEngine | str,
) -> Generator[sessionmaker[Any], None, None]:
    engine = engine if isinstance(engine, AsyncEngine) else db_engine(engine)
    maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore[call-overload]
    yield maker
    maker.close_all()


async def db_session(maker: sessionmaker[Any]) -> AsyncGenerator[AsyncSession, None]:
    session = maker()
    try:
        yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    finally:
        await session.close()


async def db_session_autocommit(
    maker: sessionmaker[Any],
) -> AsyncGenerator[AsyncSession, None]:
    session = maker()
    try:
        yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    else:
        await session.commit()
    finally:
        await session.close()


def app_config() -> AppConfig:
    return AppConfig.from_env()


async def redis_pool(redis_url: str) -> AsyncGenerator[ConnectionPool, None]:
    pool = ConnectionPool.from_url(redis_url)
    yield pool
    await pool.aclose()


async def redis_conn(pool: ConnectionPool) -> AsyncGenerator[Redis, None]:
    conn = Redis(connection_pool=pool)
    try:
        yield conn
    finally:
        await conn.aclose()
