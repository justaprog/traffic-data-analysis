import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import psycopg2
from flask import Flask
from webapplication.blueprints.home import home_bp
from webapplication.blueprints.auth import auth_bp
from webapplication.blueprints.api import api_bp
from database.connection import load_config
from database.init_database import init_database
from data_pipelines.etl import etl_bhf_to_eva

# create and configure the app
def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    # connect to postgres database
    try:
        if test_config == None:
            config = load_config()
        else:
            config = load_config(test_config)
        conn = psycopg2.connect(**config)
        # Stores the connection in your Flask app.config dictionary. 
        # This makes it easy to retrieve inside any blueprint or route by referencing current_app.config["DB_CONN"].
        print("Database connection established.")
        try:
            print(etl_bhf_to_eva(conn,'Ingolstadt Nord'))
        except Exception as e:
            print("Error while calling bhf_to_eva api:",e)
            conn.rollback()
    except Exception as e:
        print("Error connecting to the database:", e)
    finally:
        if conn:
            conn.close()

    init_database()
    # register the blueprints 
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    return app 

