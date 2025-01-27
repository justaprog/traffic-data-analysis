from flask import Blueprint, render_template, current_app

# 1. Create a Blueprint instance
home_bp = Blueprint("home_bp", __name__, template_folder="templates")

# 2. Define routes on the blueprint
@home_bp.route("/")
def index():
    # 1. Access the connection from the current Flask app
    conn = current_app.config["DB_CONN"]
    # 2. Run a query, for example:
    #    SELECT arrival_time, evaNo, path FROM Arrival
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT arrival_time, i.station as Station, path FROM Arrival ar JOIN IBNR i ON i.evaNo = ar.evaNo;")
            rows = cursor.fetchall()
            # rows will be a list of tuples
    except Exception as e:
        print("Error querying the database:", e)
        rows = []

    # 3. Render a template (for example, 'home_index.html') with the results
    return render_template("home_index.html", arrivals=rows)


