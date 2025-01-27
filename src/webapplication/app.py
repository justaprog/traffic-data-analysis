import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import psycopg2
from flask import Flask
from webapplication.blueprints.home.routes import home_bp
from webapplication.blueprints.auth.routes import auth_bp
from database.config.config import load_config

app = Flask(__name__)
# connect to postgres database
try:
    config = load_config()
    conn = psycopg2.connect(**config)
    # Stores the connection in your Flask app.config dictionary. 
    # This makes it easy to retrieve inside any blueprint or route by referencing current_app.config["DB_CONN"].
    app.config["DB_CONN"] = conn
    print("Database connection established.")
except Exception as e:
    print("Error connecting to the database:", e)


# register the blueprints 
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
