import pandas as pd
from app.models.db import engine
import datetime
from app.data_pipelines.etl import etl_changes_data, etl_planned_data
from app.database.connection import get_conn,close_conn
import matplotlib.pyplot as plt
from app.models import Ibnr, Arrival
from sqlalchemy import text
import logging
import matplotlib.dates as mdates

logger = logging.getLogger(__name__)

def delayed_arrivals(engine, evanos: list[int],next_hours: int):
    """
    This function return a panda Dataframe: (arrival_planned_time: datetime, delayed_time: minutes). 

    :param engine: sqlalchemy engine
    :param int evanos: list of station's EvaNummer
    """
    # ETL data
    db_conn = get_conn()
    now = datetime.datetime.now()
    logging.basicConfig(filename='myapp.log', level=logging.INFO)

    try:
        all_data = []
        for evano in evanos:
            for h_offset in range(next_hours):  # next next_hours
                dt = now + datetime.timedelta(hours=h_offset)
                date = dt.strftime("%y%m%d")
                hour = dt.strftime("%H")
                logger.info(f'Started:{date},{hour}')
                # ETL for each hour and station
                try:
                    etl_planned_data(db_conn, evano, date, hour)
                except Exception as e:
                    print(f"Error during etl_planned_data:{e}")
                    db_conn.rollback()
            # Update changed time
            etl_changes_data(db_conn, evano)
            # Select arrival_time and changed_time
            query = text("""
                SELECT arrival_planned_time, arrival_changed_time
                FROM arrivals
                WHERE arrival_changed_time IS NOT NULL
                AND evano = :evano
                AND arrival_planned_time > :now
            """)

            df = pd.read_sql(query, engine, params={"evano": evano , "now": now})

            # Truncate microseconds to avoid noise
            df['arrival_planned_time'] = pd.to_datetime(df['arrival_planned_time']).dt.floor('s')
            df['arrival_changed_time'] = pd.to_datetime(df['arrival_changed_time']).dt.floor('s')
            
            # Calculate delay in minutes
            df['delay_minutes'] = (df['arrival_changed_time'] - df['arrival_planned_time']).dt.total_seconds() / 60

            # Filter only delayed ones
            df = df[df['delay_minutes'] > 0]
            # label the station
            station_name = Ibnr.get_station_by_evano(evano)
            df['station'] = station_name

            all_data.append(df[['arrival_planned_time', 'delay_minutes', 'station']])
    finally:
        close_conn(db_conn)

    full_df = pd.concat(all_data)
    # Plot
    plt.figure(figsize=(12, 6))
    for station_name, station_df in full_df.groupby('station'):
        plt.scatter(station_df['arrival_planned_time'], station_df['delay_minutes'], label=f"Station {station_name}")
    # Format x-axis to yy/mm/dd HH/MM
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y/%m/%d %H:%M'))

    plt.title(f"Delay Trends Over Time (Next {next_hours} Hours)")
    plt.xlabel("Planned Arrival Time")
    plt.ylabel("Delay (minutes)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    # To print in csv file
    #filename = f"delayed_arrivals_{evano}_{datetime.datetime.now()}.csv"
    #df[['arrival_planned_time', 'delay_minutes']].to_csv(filename, index=False)

if __name__ == "__main__":
    # Berlin hbf:8098160, München hbf:8000261, Frankfurt am Main hbf:8000105
    delayed_arrivals(engine, [8098160,8000261,8000105],6)

