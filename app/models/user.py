from typing import TYPE_CHECKING

from sqlalchemy import String,Integer,DateTime,Boolean, func
from sqlalchemy.orm import Mapped,mapped_column, relationship
from database import Base


if TYPE_CHECKING:
    from app.models.todo import Todo 

class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(Integer,primary_key= True, autoincrement=True)
    username : Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    email : Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    password : Mapped[str] = mapped_column(String(200),nullable=False)
    todos : Mapped[list["Todo"]] = relationship(back_populates="author", cascade="all,delete-orphan")
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    