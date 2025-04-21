# traffic-data-analysis
## Introduction
This project uses Deutsche Bahn's Timetables-API (https://developers.deutschebahn.com/db-api-marketplace/apis/product/timetables) to analyse traffic. This includes: ETL-Prozess, data visualization and analytics using Machine Learning Algorithms.
## Demo
Here’s what the traffic information page looks like:

![Traffic Page Screenshot](data/images/demo.png)
## Setup 
There need to be a file named .env in rootfolder to set up enviroment variables. 
### Database Connection
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
## How to start
### With python
Create virtual environment for Linux and WSL(pip & virtualenv): \
run: `pip install -U pip` \
run: `sudo apt install python3 python3-pip` \
run: `pip install virtualenv` \
run: `virtualenv venv`  # erstellt im aktuellen Ordner einen Ordner 'venv' mit der virtuellen Umgebung\
run: `source venv/bin/activate`   # danach erscheint ein (venv) vor dem Command Prompt\
run: `pip install -r requirements.txt` \
run: `flask --app src/webapplication run --debug` from root to start web application.
go to: `http://localhost:5000/`
### With Docker
run: `docker compose up -d --build` \
go to: `http://localhost:5000/`
## Tools
Database: PostgreSQL.  
Frontend: HTML/CSS, Javascript.  
Backend: Python, Flask
## Data
Deutsche Bahn's Timetables-API, Interne Bahnhofsnummer(IBNR).
