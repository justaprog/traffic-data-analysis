from flask import Blueprint, render_template, current_app
import psycopg2

from database.connection import get_conn,close_conn
from data_pipelines.etl import etl_changes_data,etl_planned_data 
# Import 
from webapplication.blueprints.api import api_bp


# Define routes on the blueprint
@api_bp.route("/arrival")
def arrival():
    #   Access the connection from the current Flask app
    db_conn = get_conn()
    #    Run etl process
    if db_conn:
        # ETL process
        try:
            etl_planned_data(db_conn,8098160, 250423, 21)
        except Exception as e:
            print("Error during etl process:",e)
            db_conn.rollback()
        # Retrieve arrival data from database
        try:
            with db_conn.cursor() as cursor:
                cursor.execute("SELECT arrival_time, line, i.station as Station, path FROM Arrival ar " \
                "JOIN IBNR i ON i.evaNo = ar.evaNo " \
                "ORDER BY arrival_time;")
                rows = cursor.fetchall() # rows will be a list of tuples
        except Exception as e:
            print("Error querying the database:", e)
            db_conn.rollback()
            rows = []
        finally:
            if db_conn:
                db_conn.close()
    # Render a template (for example, 'home_index.html') with the results
    return render_template("api/arrival.html", arrivals=rows)

