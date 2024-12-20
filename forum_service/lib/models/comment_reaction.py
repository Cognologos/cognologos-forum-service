# from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from .abc import AbstractModel
#
#
# class CommentReaction(AbstractModel):
#     __tablename__ = "comment_reactions"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     post_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), index=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
#     reaction_type: Mapped[str] = mapped_column(String(10))
#
#     post: Mapped["Comment"] = relationship("Comment", back_populates="reactions")
#     user: Mapped["User"] = relationship("User", back_populates="reactions")
#
#     __table_args__ = (UniqueConstraint("comment_id", "user_id", name="unique_comment_user_reaction"),)
