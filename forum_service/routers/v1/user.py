from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from forum_service.core.dependencies.fastapi import db_session
from forum_service.lib.schemas.users import UserCreate, UserResponse
from forum_service.lib.db.user import get_user_by_username_or_email, create_user_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, session: AsyncSession = Depends(db_session)):

    existing_user = await get_user_by_username_or_email(user.username, user.email, session)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        new_user = await create_user_db(user, user.password, session)
        return new_user
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to register user")
