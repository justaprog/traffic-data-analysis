from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from .base import Base

class Ibnr(Base):
    __tablename__ = "ibnrs"

    evano: Mapped[int] = mapped_column(Integer, primary_key=True)
    station: Mapped[str] = mapped_column(String(255), unique=True)
