from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Text, ForeignKey, String, text
import datetime
from .base import Base
from .db import engine

class Arrival(Base):
    __tablename__ = "arrivals"

    arrival_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    arrival_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    line: Mapped[str] = mapped_column(String(50))
    planned_platform: Mapped[str] = mapped_column(String(50))
    path: Mapped[str] = mapped_column(Text)
    evano: Mapped[int] = mapped_column(ForeignKey("ibnrs.evano"))

    @classmethod
    def get_data_by_evano(cls,evano):
        with engine.connect() as conn:
            stmt = text("""

        SELECT DISTINCT arrival_time, line, i.station as Station, path FROM arrivals ar
        JOIN IBNRs i ON i.evano = ar.evano
        WHERE i.evano = :evano 
        ORDER BY arrival_time;
                        """)
            try:
                result = conn.execute(stmt,{"evano": evano}).fetchall()
            except Exception as e:
                print("Error querying the database:", e)
                conn.rollback()
        return result
