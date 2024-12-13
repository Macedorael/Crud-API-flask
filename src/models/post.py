from sqlalchemy.orm import Mapped, mapped_column 
import sqlalchemy as sa
from datetime import datetime
from src.models.base import db

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))

    def __repr__(self):
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
    