from __init__ import create_app

app = create_app()
app.run(host="0.0.0.0", port = 8000)