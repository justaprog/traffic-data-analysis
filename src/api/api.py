import requests
import os
from dotenv import load_dotenv

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

print(response.text)
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)

