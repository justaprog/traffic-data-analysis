from flask import Blueprint, render_template, current_app
import psycopg2

from database.config import load_config
from data_pipelines.etl import etl_changes_data,etl_planned_data 

from webapplication.blueprints.home import home_bp

#  Define routes on the blueprint
@home_bp.route("/")
def index():
    return render_template('home/index.html')