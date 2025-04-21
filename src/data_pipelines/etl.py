import sys
import os

sys.path.append(os.path.abspath("./src/database/config"))

import psycopg2
from .collect import collect_planned_data, collect_changes_data
import xml.etree.ElementTree as ET
from datetime import datetime

from config import load_config

def etl_planned_data(cursor,evaNo, date, hour):
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
    data = collect_planned_data(evaNo, date, hour)
    #print(data)
    root = ET.fromstring(data)
    station_name = root.attrib["station"]
    try:
        cursor.execute(f"INSERT INTO IBNR VALUES ({evaNo},'{station_name}')")
    except:
        print (f"EvaNo:{evaNo} is in the database")
    # Find all Objects 
    for object in root.findall("s"):
        #Find all arrival path
        ar_elements = object.findall("ar")

        for ar in ar_elements:
            # Access attributes of each <ar> element
            id = ar.get("id",'NULL')
            pt = ar.attrib.get("pt", 'NULL')
            pp = ar.attrib.get("pp", 'NULL')
            ppth = ar.attrib.get("ppth", 'NULL')
            timestamp = datetime.strptime(pt, "%y%m%d%H%M")
            try:
                cursor.execute(f"INSERT INTO Arrival VALUES (DEFAULT,'{timestamp}','{pp}','{ppth}',{evaNo}) ON CONFLICT DO NOTHING;")
            except psycopg2.DatabaseError as e:
                print(f"Database error during insert: {e}")
        # Find all Departure
        dp_elements = object.findall("dp")
        for dp in dp_elements:
            # Access attributes of each <dp> element
            id = dp.get("id",'NULL')
            pt = dp.attrib.get("pt", 'NULL')
            pp = dp.attrib.get("pp", 'NULL')
            ppth = dp.attrib.get("ppth", 'NULL')
            timestamp = datetime.strptime(pt, "%y%m%d%H%M")
            try:
                cursor.execute(f"INSERT INTO Departure VALUES (DEFAULT,'{timestamp}','{pp}','{ppth}',{evaNo}) ON CONFLICT DO NOTHING;")
            except psycopg2.DatabaseError as e:
                print(f"Database error during insert: {e}")

def etl_changes_data(cursor, evaNo):
    """
    Beschreibung
    Returns a Timetable object (see Timetable) that contains all known changes for the station given by evaNo.

    The data includes all known changes from now on until ndefinitely into the future. Once changes become obsolete (because their trip 
    departs from the station) they are removed from this resource.

    Changes may include messages. On event level, they usually contain one or more of the 'changed' attributes ct, cp, cs or cpth. 
    Changes may also include 'planned' attributes if there is no associated planned data for the change (e.g. an unplanned stop or trip).

    Full changes are updated every 30s and should be cached for that period by web caches.

    string ct =  "Changed time. New estimated or actual departure or arrival time. The time, in ten digit 'YYMMddHHmm' format, 
                  e.g. '1404011437' for 14:37 on April the 1st of 2014.
    string cp = "Changed platform."
    enum cs =   "Event status. 
            * p - PLANNED The event was planned. This status is also used when the cancellation of an event has been revoked. 
            * a - ADDED The event was added to the planned data (new stop). 
            * c - CANCELLED The event was canceled (as changedstatus, can apply to planned and added stops). "
    string cpth = "Changed path."


    """
    data = collect_changes_data(evaNo)
    root = ET.fromstring(data)
    station_name = root.attrib["station"]
    try:
        cursor.execute(f"INSERT INTO IBNR VALUES ({evaNo},'{station_name}')")
    except:
        print (f"EvaNo:{evaNo} is in the database")

    for object in root.findall("s"):
        ar_elements = object.findall("ar")
        for ar in ar_elements:
            # Access attributes of each <ar> element
            ct = ar.attrib.get("ct", 'NULL')
            cp = ar.attrib.get("cp", 'NULL')
            cs = ar.attrib.get("cs", 'NULL')
            cpth = ar.attrib.get("cpth", 'NULL')
            print(ct,cp,cs,cpth)

        #print(object.findall("ar").attrib.get("ct",None))
    """
    cursor.execute("SELECT * FROM IBNR;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    """

if __name__ == "__main__":
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                #etl_planned_data(cur,8000105, 250122, 21)
                cur.execute("SELECT * FROM Departure")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Database error: {error}")
    finally:
        if conn:
            conn.close()

