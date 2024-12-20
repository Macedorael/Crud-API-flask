import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import db



class Role(db.Model): 
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(30), unique=True, nullable=False)
    user: Mapped[list["user.User"]] = relationship(back_populates="role")
    
    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r}, active={self.active!r})"