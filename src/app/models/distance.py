from sqlalchemy import Numeric, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Distance(Base):
    __tablename__ = "distances"

    distance_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    evano_1: Mapped[int] = mapped_column(ForeignKey("ibnrs.evano"), nullable=False)
    evano_2: Mapped[int] = mapped_column(ForeignKey("ibnrs.evano"), nullable=False)
    distance: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    __table_args__ = (UniqueConstraint('evano_1', 'evano_2', name='unique_station_pair'),)  