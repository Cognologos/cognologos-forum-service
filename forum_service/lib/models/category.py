from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel


if TYPE_CHECKING:
    from .post import PostModel


class CategoryModel(AbstractModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    posts: Mapped[list["PostModel"]] = relationship("PostModel", back_populates="category")
