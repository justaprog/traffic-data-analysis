from flask import Blueprint, render_template, current_app
import psycopg2

from database.connection import get_conn,close_conn
from data_pipelines.etl import etl_changes_data,etl_planned_data 
# Import 
from webapplication.blueprints.api import api_bp

# 2. Define routes on the blueprint
@api_bp.route("/departure")
def departure():
    #   Access the connection from the current Flask app
    config = load_config()

    evaNo = "8000261"    # station's Evanummer
    date = "250424"   # Date in YYMMDD
    hour = "01"   
    #    Run etl process
    try:
        with psycopg2.connect(**config) as conn:
            try:
                etl_planned_data(conn,evaNo, date, hour) 
            except Exception as e:
                print("Error during etl process:",e)
            # rows will be a list of tuples
    except Exception as e:
        print("Error connecting the database:", e)
    finally:
        if conn:
            conn.close()
    #   Run a query, for example:
    #   SELECT arrival_time, evaNo, path FROM Arrival
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT departure_time, line, i.station as Station, path FROM Departure ar " \
                "JOIN IBNR i ON i.evaNo = ar.evaNo " \
                "ORDER BY departure_time;")
                rows = cursor.fetchall()
                # rows will be a list of tuples
    except Exception as e:
        print("Error querying the database:", e)
        rows = []
    finally:
        if conn:
            conn.close()

    # Render a template (for example, 'home_index.html') with the results
    return render_template("api/departure.html", departure=rows)
