import requests
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

# Load environment variables
load_dotenv()

# Access API keys
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/8000105"

headers = {
    "DB-Client-Id": client_id,
    "DB-Api-Key": client_secret,
    "accept": "application/xml"
}

response = requests.get(url, headers=headers)
# get data
xml_data = response.text
# Parse the XML
root = ET.fromstring(xml_data)
station = root.attrib.get("station")
eva = root.attrib.get("eva")
print(f"Stop ID: {station}, EVA: {eva}")



#print(response.text)
"""
with open("data/timetable.xml", "w") as file:
    file.write(xml_data)

print("XML file saved as 'timetable.xml'")
"""
"""
if response.status_code == 200:
    print("Success, here are API's Headers:", response.headers)
else:
    print("Error:", response.status_code, response.text)
"""
