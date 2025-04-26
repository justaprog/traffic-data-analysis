from flask import Blueprint, render_template, current_app
import psycopg2

from app.database.connection import load_config
from app.data_pipelines.etl import etl_changes_data,etl_planned_data 

from app.blueprints.home import home_bp

#  Define routes on the blueprint
@home_bp.route("/")
def index():
    return render_template('home/index.html')