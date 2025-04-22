from flask import Blueprint, render_template, current_app
import psycopg2

from database.config import load_config
from data_pipelines.etl import etl_changes_data,etl_planned_data 
# 1. Create a Blueprint instance
from webapplication.blueprints.api import api_bp
# 2. Define routes on the blueprint
@api_bp.route("/arrival")
def arrival():
    #   Access the connection from the current Flask app
    config = load_config()
    #    Run etl process
    try:
        with psycopg2.connect(**config) as conn:
            try:
                etl_planned_data(conn,8004145, 250422, 22)
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
                cursor.execute("SELECT arrival_time, line, i.station as Station, path FROM Arrival ar " \
                "JOIN IBNR i ON i.evaNo = ar.evaNo " \
                "ORDER BY arrival_time;")
                rows = cursor.fetchall()
                # rows will be a list of tuples
    except Exception as e:
        print("Error querying the database:", e)
        rows = []
    finally:
        if conn:
            conn.close()
    # Render a template (for example, 'home_index.html') with the results
    return render_template("api/arrival.html", arrivals=rows)

# 2. Define routes on the blueprint
@api_bp.route("/departure")
def departure():
    #   Access the connection from the current Flask app
    config = load_config()
    #    Run etl process
    try:
        with psycopg2.connect(**config) as conn:
            try:
                etl_planned_data(conn,8000261, 250422, 22)
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
