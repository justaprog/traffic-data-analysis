# traffic-data-analysis
## Introduction
This project uses Deutsche Bahn's Timetables-API (https://developers.deutschebahn.com/db-api-marketplace/apis/product/timetables) to analyse traffic. This includes: ETL-Prozess, data visualization and analytics using Machine Learning Algorithms.
## Demo
Here’s what the traffic information page looks like:

![Traffic Page Screenshot](data/images/demo.png)
## Setup 
There need to be a file named .env in rootfolder to set up enviroment variables. 
### Database Connection
<<<<<<< HEAD
To connect to the postgreSQL database, .env need to contain \
"
DB_HOST=YOURHOST
DB_NAME=YOURNAME
DB_USER=YOURUSER
DB_PASSWORD=YOURPASSWORD
"
### Deutsche Bahn API
To access the API, .env need to contain
"
CLIENT_ID = "Your API ID"
CLIENT_SECRET = "Your API Secret"
"
### Install Docker Engine (Optional)
https://docs.docker.com/engine/install/ubuntu/
=======
To connect to the postgreSQL database, there need to be a file named database.ini in src/database/config containing \
[postgresql] \
host=localhost \
database=suppliers \
user=YourUsername \
password=YourPassword
### Deutsche Bahn API
To access the API, there need to be a file named .env in src/data_pipelines containing \

CLIENT_ID = "Your API ID"\
CLIENT_SECRET = "Your API Secret" 
>>>>>>> 0df7cdbdc478d2a1dfe372341c83f00fe51ecaef
## How to start
### With python
Create virtual environment for Linux and WSL(pip & virtualenv): \
run: `pip install -U pip` \
run: `sudo apt install python3 python3-pip` \
run: `pip install virtualenv` \
run: `virtualenv venv`  # erstellt im aktuellen Ordner einen Ordner 'venv' mit der virtuellen Umgebung\
run: `source venv/bin/activate`   # danach erscheint ein (venv) vor dem Command Prompt\
run: `pip install -r requirements.txt` \
<<<<<<< HEAD
run: `python src/webapplication/app.py` from root to start web application.
### With Docker


=======
run: `python src/webapplication/run.py` from root to start web application.
>>>>>>> 0df7cdbdc478d2a1dfe372341c83f00fe51ecaef
## Tools
Database: PostgreSQL.  
Frontend: Html/css, Javascript, Flask.  
Backend: Python.  
## Data
Deutsche Bahn's Timetables-API, Interne Bahnhofsnummer(IBNR).
