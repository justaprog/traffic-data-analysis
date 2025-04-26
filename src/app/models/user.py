from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, DateTime
import datetime 
from .base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable = False)
    last_name: Mapped[str] = mapped_column(String(50), nullable = False)
    user_name: Mapped[str] = mapped_column(String(20), nullable = False)
    password: Mapped[str] = mapped_column(String(255), nullable = False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default = datetime.datetime.now)
    # to print
    def __repr__(self):
        return f"User(id={self.user_id!r}, full name={self.first_name!r} {self.last_name!r}, created_at = {self.created_at!r})"

if __name__ == '__main__':
    duong = User(first_name = "Duong", last_name = "Tran", user_name="duong", password = "test123")
    print(duong)

