from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel


if TYPE_CHECKING:
    from .post import PostModel
    from .user import UserModel


class PostReactionModel(AbstractModel):
    __tablename__ = "post_reactions"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    reaction_type: Mapped[str] = mapped_column(String(10))

    post: Mapped["PostModel"] = relationship("PostModel", back_populates="reactions")
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="reactions")

    __table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_post_user_reaction"),)
