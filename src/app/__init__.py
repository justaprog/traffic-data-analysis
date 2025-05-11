import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import psycopg2
from flask import Flask
from app.blueprints.home import home_bp
from app.blueprints.auth import auth_bp
from app.blueprints.api import api_bp
from app.database.connection import load_config
from app.database.init_database import init_database
from app.data_pipelines.etl import etl_bhf_to_eva
from app.models import init_db

# create and configure the app
def create_app():
    app = Flask(__name__, instance_relative_config = True)
    # Initialize Database
    with app.app_context():
        init_db(drop_tables=False)
        print("Database connection succeeded")

    # register the blueprints 
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    return app 

