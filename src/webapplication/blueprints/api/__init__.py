from flask import Blueprint

api_bp = Blueprint("api_bp", __name__, url_prefix = "/api", template_folder='templates')

from webapplication.blueprints.api import arrival, departure