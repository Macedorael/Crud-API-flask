from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from .base import db

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped[list["role.Role"]] = relationship(back_populates="user")
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"