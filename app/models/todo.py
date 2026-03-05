from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, DateTime, func
from database import Base

if TYPE_CHECKING:
    from app.models.user import User

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    author: Mapped["User"] = relationship(back_populates="todos")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())