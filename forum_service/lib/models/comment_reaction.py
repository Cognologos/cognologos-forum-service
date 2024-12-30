from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel


if TYPE_CHECKING:
    from .comment import CommentModel


class CommentReactionModel(AbstractModel):
    __tablename__ = "comment_reactions"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), index=True)
    reaction_type: Mapped[str] = mapped_column(String(10))

    comment: Mapped["CommentModel"] = relationship("CommentModel", back_populates="comment_reaction")

    __table_args__ = (UniqueConstraint("comment_id", "user_id", name="unique_comment_user_reaction"),)
