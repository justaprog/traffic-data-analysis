from flask import Blueprint, render_template, current_app
import psycopg2

from app.database.connection import get_conn,close_conn
from app.data_pipelines.etl import etl_changes_data,etl_planned_data,etl_bhf_to_eva

from app.blueprints.api import api_bp
from app.models import Ibnr, Arrival, Departure


# Define routes on the blueprint
@api_bp.route("/departure")
def departure():
    #   Access the connection from the current Flask app
    db_conn = get_conn()
    #    Run etl process
    if db_conn:
        # ETL process
        try:
            etl_planned_data(db_conn,8098160, 250426, "12" )
        except Exception as e:
            print("Error during etl process:",e)
            db_conn.rollback()
        # Retrieve departure data from database
        try:
            with db_conn.cursor() as cursor:
                cursor.execute("SELECT departure_time, line, i.station as Station, path FROM departures ar " \
                "JOIN IBNRs i ON i.evaNo = ar.evaNo " \
                "ORDER BY departure_time;")
                rows = cursor.fetchall() # rows will be a list of tuples
        except Exception as e:
            print("Error querying the database:", e)
            db_conn.rollback()
            rows = []
        finally:
            if db_conn:
                db_conn.close()
    # Render a template (for example, 'home_index.html') with the results
    return render_template("api/departure.html", departures=rows)

@api_bp.route("/v2/departure/<evano>/<date>/<hour>")
def departure_v2(evano,date,hour):
    db_conn = get_conn()
    f_date = date.replace("-","")
    if db_conn:
        try: 
            etl_planned_data(db_conn, evano,f_date,hour)
        except Exception as e:
            print("Error during etl process:",e)
            db_conn.rollback()
    try:
        rows = Departure.get_data_by_evano(evano)
    except Exception as e:
        print("Error querying the database:", e)
        db_conn.rollback()
        rows = []
    finally: 
        if db_conn:
            db_conn.close()
    return render_template("api/departure.html",departures=rows)
