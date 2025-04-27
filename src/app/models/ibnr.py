from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, text
from .base import Base
from .db import engine

class Ibnr(Base):
    __tablename__ = "ibnrs"

    evano: Mapped[int] = mapped_column(Integer, primary_key=True)
    station: Mapped[str] = mapped_column(String(255), unique=True)

    @classmethod
    def get_station_by_evano(cls, evano: int):
        with engine.connect() as conn:
            stmt = text("SELECT station FROM ibnrs WHERE evano = :evano")
            result = conn.execute(stmt,{"evano":evano}).fetchone()
        if result:
            return result[0]
        return None

