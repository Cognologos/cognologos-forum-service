from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import or_

from forum_service.lib.models.user import User
from forum_service.lib.schemas.users import UserCreate


async def get_user_by_username_or_email(username: str, email: str, session: AsyncSession) -> User | None:
    stmt = select(User).where(or_(User.username == username, User.email == email))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user_db(user: UserCreate, hashed_password: str, session: AsyncSession) -> User:
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except Exception as e:
        await session.rollback()
        raise e
