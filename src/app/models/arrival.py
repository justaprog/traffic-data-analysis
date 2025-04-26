from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Text, ForeignKey, String
import datetime
from .base import Base

class Arrival(Base):
    __tablename__ = "arrivals"

    arrival_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    arrival_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    line: Mapped[str] = mapped_column(String(50))
    planned_platform: Mapped[str] = mapped_column(String(50))
    path: Mapped[str] = mapped_column(Text)
    evano: Mapped[int] = mapped_column(ForeignKey("ibnrs.evano"))