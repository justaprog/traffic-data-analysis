# traffic-data-analysis
## Introduction
This project use Deutsche Bahn's Timetables-API (https://developers.deutschebahn.com/db-api-marketplace/apis/product/timetables) to analyse traffic. This includes: ETL-Prozess,data visualization and analysis using Machine Learning Algorithms.
## How to start
Create virtual environment for Linux and WSL(pip & virtualenv): __
run: `pip install -U pip` __
run: `sudo apt install python3 python3-pip` __
run: `pip install virtualenv` __ 
run: `virtualenv venv` __ # erstellt im aktuellen Ordner einen Ordner 'venv' mit der virtuellen Umgebung
run: `source venv/bin/activate` __  # danach erscheint ein (venv) vor dem Command Prompt
run: `pip install -r requirements.txt` __ 
run: `sudo apt-get install libpq-dev python3-dev` __
## Database
Postgresql
## Data
Deutsche Bahn's Timetables-API, Interne Bahnhofsnummer(IBNR), 