from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .abc import AbstractModel


class User(AbstractModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")

    reactions: Mapped[list["PostReaction"]] = relationship(
        "PostReaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # comment_reactions: Mapped[list["CommentReaction"]] = relationship(
    #     "CommentReaction",
    #     back_populates="user",
    #     cascade="all, delete-orphan"
    # )