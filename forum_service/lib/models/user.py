from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel


if TYPE_CHECKING:
    from .comment import CommentModel
    from .post import PostModel
    from .post_reaction import PostReactionModel


class UserModel(AbstractModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]

    posts: Mapped[list["PostModel"]] = relationship("PostModel", back_populates="author")
    comments: Mapped[list["CommentModel"]] = relationship("CommentModel", back_populates="author")
    reactions: Mapped[list["PostReactionModel"]] = relationship(
        "PostReactionModel", back_populates="user", cascade="all, delete-orphan"
    )
