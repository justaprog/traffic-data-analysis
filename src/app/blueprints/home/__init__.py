from flask import Blueprint

home_bp = Blueprint("home_bp",__name__, url_prefix = "/", template_folder ="templates")

from app.blueprints.home import routes