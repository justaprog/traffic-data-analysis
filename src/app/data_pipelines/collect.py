import requests
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Access API keys
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def collect_eva_from_bhf(bhf):
    """Request a api call to get evaNummer from Bahnhof"""
    url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/{bhf}"
    headers = {
        "DB-Client-Id": client_id,
        "DB-Api-Key": client_secret,
        "accept": "application/xml"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Success, here are API's Headers:", response.headers)
    else:
        print("Error:", response.status_code, response.text)
        if response.status_code == 404:
            print("Please try another name")

    # get data
    xml_data = response.text

    return xml_data

def collect_planned_data(evaNo, date, hour):
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
    url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/{evaNo}/{date}/{hour}"

    headers = {
        "DB-Client-Id": client_id,
        "DB-Api-Key": client_secret,
        "accept": "application/xml"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Success, here are API's Headers:", response.headers)
    else:
        print("Error:", response.status_code, response.text)
        if response.status_code == 404:
            print("Please try another date")

    # get data
    xml_data = response.text
    """
    with open("data/timetable.xml", "w") as file:
        file.write(xml_data)

    print("XML file saved as 'timetable.xml'")
    """

    return xml_data

def collect_changes_data(evaNo):
    """
    Beschreibung
    Returns a Timetable object (see Timetable) that contains all known changes for the station given by evaNo.

    The data includes all known changes from now on until ndefinitely into the future. Once changes become obsolete (because their trip departs from the station) they are removed from this resource.

    Changes may include messages. On event level, they usually contain one or more of the 'changed' attributes ct, cp, cs or cpth. Changes may also include 'planned' attributes if there is no associated planned data for the change (e.g. an unplanned stop or trip).

    Full changes are updated every 30s and should be cached for that period by web caches.
    """
    url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/{evaNo}"
    headers = {
        "DB-Client-Id": client_id,
        "DB-Api-Key": client_secret,
        "accept": "application/xml"
    }
    response = requests.get(url, headers=headers)
    """
    if response.status_code == 200:
        print("Success, here are API's Headers:", response.headers)
    else:
        print("Error:", response.status_code, response.text)
    """
    # get data
    xml_data = response.text

    return xml_data


if __name__ == "__main__":
    print(collect_planned_data(8000105, 250419, 21))
    #print(collect_changes_data(8000105))