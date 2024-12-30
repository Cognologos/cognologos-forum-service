from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel


if TYPE_CHECKING:
    from .post import PostModel


class CommentModel(AbstractModel):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int]
    likes: Mapped[int] = mapped_column(default=0)
    dislikes: Mapped[int] = mapped_column(default=0)

    post: Mapped["PostModel"] = relationship("PostModel", back_populates="comments")
