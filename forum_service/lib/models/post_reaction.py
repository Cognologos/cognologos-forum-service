from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .abc import AbstractModel


class PostReaction(AbstractModel):
    __tablename__ = "post_reactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    reaction_type: Mapped[str] = mapped_column(String(10))

    post: Mapped["Post"] = relationship("Post", back_populates="reactions")
    user: Mapped["User"] = relationship("User", back_populates="reactions")

    __table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_post_user_reaction"),)
