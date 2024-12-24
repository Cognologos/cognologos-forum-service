from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel
from .post_reaction import PostReactionModel


if TYPE_CHECKING:
    from .category import CategoryModel
    from .comment import CommentModel
    from .user import UserModel


class PostModel(AbstractModel):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    author: Mapped["UserModel"] = relationship("UserModel", back_populates="posts")
    category: Mapped["CategoryModel"] = relationship("CategoryModel", back_populates="posts")
    comments: Mapped[list["CommentModel"]] = relationship("CommentModel", back_populates="post")
    reactions: Mapped[list["PostReactionModel"]] = relationship("PostReaction", back_populates="post")
