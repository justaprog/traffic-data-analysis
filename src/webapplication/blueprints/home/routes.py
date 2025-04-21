from flask import Blueprint, render_template, current_app
import psycopg2

from database.config.config import load_config
from data_pipelines.etl import etl_changes_data,etl_planned_data 
# 1. Create a Blueprint instance
home_bp = Blueprint("home_bp", __name__, template_folder="templates")

# 2. Define routes on the blueprint
@home_bp.route("/")
def index():
    #   Access the connection from the current Flask app
    config = load_config()
    #    Run etl process
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                try:
                    etl_planned_data(cursor,8000105, 250421, 21)
                except Exception as e:
                    print(e)
                # rows will be a list of tuples
    except Exception as e:
        print("Error querying the database:", e)

    #   Run a query, for example:
    #   SELECT arrival_time, evaNo, path FROM Arrival
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT arrival_time, i.station as Station, path FROM Arrival ar " \
                "JOIN IBNR i ON i.evaNo = ar.evaNo " \
                "ORDER BY arrival_time;")
                rows = cursor.fetchall()
                # rows will be a list of tuples
    except Exception as e:
        print("Error querying the database:", e)
        rows = []

    # Render a template (for example, 'home_index.html') with the results
    return render_template("home_index.html", arrivals=rows)


