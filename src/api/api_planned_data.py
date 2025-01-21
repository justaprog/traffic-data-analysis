import requests
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

# Load environment variables
load_dotenv()

# Access API keys
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

evaNo = 8000105
date = 250121
hour = 10

url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/{evaNo}/{date}/{hour}"

headers = {
    "DB-Client-Id": client_id,
    "DB-Api-Key": client_secret,
    "accept": "application/xml"
}
"""
Beschreibung
Returns a Timetable object (see Timetable) that contains planned data for the specified station (evaNo) within the hourly time slice 
given by date (format YYMMDD) and hour (format HH). The data includes stops for all trips that arrive or depart within that slice. 
There is a small overlap between slices since some trips arrive in one slice and depart in another.

Planned data does never contain messages. On event level, planned data contains the 'plannned' attributes pt, pp, ps and ppth while 
the 'changed' attributes ct, cp, cs and cpth are absent.

Planned data is generated many hours in advance and is static, i.e. it does never change. It should be cached by web caches.public 
interface allows access to information about a station.
"""
response = requests.get(url, headers=headers)

# get data
xml_data = response.text

print(xml_data)

"""
if response.status_code == 200:
    print("Success, here are API's Headers:", response.headers)
else:
    print("Error:", response.status_code, response.text)
"""
