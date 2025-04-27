from sqlalchemy import create_engine,text, MetaData
from dotenv import load_dotenv
import os 

from .base import Base
from .ibnr import Ibnr
from .arrival import Arrival
from .departure import Departure
from .distance import Distance
from .user import User
from .db import engine

# init db 
def init_db(drop_tables = False):
    if drop_tables:
        commands = """
            DROP TABLE IF EXISTS users CASCADE;
            DROP TABLE IF EXISTS distances CASCADE;
            DROP TABLE IF EXISTS departures CASCADE;
            DROP TABLE IF EXISTS arrivals CASCADE;
            DROP TABLE IF EXISTS ibnrs CASCADE;
        """
        with engine.connect() as conn:
            result = conn.execute(text(commands))
            conn.commit()
    # Emitting DDL to the database from an ORM mapping
    Base.metadata.create_all(engine)