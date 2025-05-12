import sys
import os

import psycopg2
from .collect import collect_planned_data, collect_changes_data, collect_eva_from_bhf
import xml.etree.ElementTree as ET
from datetime import datetime

from app.database.connection import load_config,get_conn

def etl_bhf_to_eva(db_conn, bhf):
    data = collect_eva_from_bhf(bhf)
    root = ET.fromstring(data)
    try:
        evaNo = root.find('station').get('eva')
    except Exception as e:
        print("Failed request, Please try different bahnhof name")
    else:
        try:
            with db_conn.cursor() as cursor:
                cursor.execute(f"INSERT INTO ibnrs VALUES ({evaNo},'{bhf}')")
            print(f"Insert ({evaNo},{bhf}) successful")
            db_conn.commit()
        except Exception as e:
            print(f"Etl_bhf_to_eva:({evaNo},{bhf}) is in the database")
            db_conn.rollback()
        finally:
            if db_conn:
                db_conn.close()
    

def etl_planned_data(conn,evaNo, date, hour):
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
    # If IBNR not in database, insert
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO ibnrs VALUES ({evaNo},'{station_name}')")
        conn.commit()
    except:
        print (f"EvaNo:{evaNo} is in the database")
        conn.rollback() # rollback the failed insertion

    # Find all Objects 
    for object in root.findall("s"):
        #Find all arrivals and process arrivals
        ar_elements = object.findall("ar")
        id = object.attrib.get("id")
        for ar in ar_elements:
            # Access attributes of each <ar> element
            line = ar.attrib.get("l",'Not Available') # Line
            pt = ar.attrib.get("pt", 'NULL') # planned time
            pp = ar.attrib.get("pp", 'NULL') #  planned planned_platform
            ppth = ar.attrib.get("ppth", 'NULL') # planned path
            if pt is None:
                continue
            if pp is None:
                continue
            if ppth is None:
                continue    
            pt_timestamp = datetime.strptime(pt, "%y%m%d%H%M")
                        # Truncate Microseconds
            pt_timestamp = pt_timestamp.replace(microsecond=0)
            # Truncate seconds
            pt_timestamp = pt_timestamp.replace(second=0)

            query = """
                    INSERT INTO arrivals (arrival_id, arrival_planned_time, line, planned_platform, path, evaNo)
                    VALUES (%s,%s,%s, %s, %s, %s);
                    """
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (id,pt_timestamp, line, pp, ppth, evaNo))
                conn.commit()
            except psycopg2.DatabaseError as e:
                print(f"Database error during insert: {e}")
                conn.rollback()

        # Find all Departures and process departures
        dp_elements = object.findall("dp")
        for dp in dp_elements:
            # Access attributes of each <dp> element
            line = dp.attrib.get("l",'Not Available')
            pt = dp.attrib.get("pt", 'NULL')
            pp = dp.attrib.get("pp", 'NULL')
            ppth = dp.attrib.get("ppth", 'NULL')
            # Skip invalid entries
            if pt is None:
                print("Skipping element with missing 'pt'")
                continue
            
            timestamp = datetime.strptime(pt, "%y%m%d%H%M")
            query = """
                    INSERT INTO departures (departure_id,departure_planned_time, line, planned_platform, path, evaNo)
                    VALUES (%s,%s, %s, %s, %s, %s);
                    """
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (id,timestamp, line, pp, ppth, evaNo))
                conn.commit()
            except psycopg2.DatabaseError as e:
                print(f"Database error during insert: {e}")
                conn.rollback()
                

def etl_changes_data(conn, evaNo):
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
    #print(data)
    root = ET.fromstring(data)
    station_name = root.attrib["station"]
    # If IBNR not in database, insert
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO ibnrs VALUES ({evaNo},'{station_name}')")
        conn.commit()
    except:
        print (f"EvaNo:{evaNo} is in the database")
        conn.rollback() # rollback the failed insertion

    # Find all Objects 
    for object in root.findall("s"):
        #Find all arrivals and process arrivals
        ar_elements = object.findall("ar")
        id = object.attrib.get("id")
        for ar in ar_elements:
            ct = ar.attrib.get("ct", "NULL") # planned time  
            if ct == "NULL":
                print("Skipping element with missing 'ct'")
                continue
            # parse in datetime
            ct_timestamp = datetime.strptime(ct, "%y%m%d%H%M")
            # Truncate Microseconds
            ct_timestamp = ct_timestamp.replace(microsecond=0)
            # Truncate seconds
            ct_timestamp = ct_timestamp.replace(second=0)

            query = """
                UPDATE arrivals 
                SET arrival_changed_time = %s 
                WHERE arrival_id = %s 
                AND arrival_planned_time IS DISTINCT FROM %s;
            """
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (ct_timestamp, id,ct_timestamp))
                conn.commit()
            except psycopg2.DatabaseError as e:
                print(f"Database error during insert: {e}")
                conn.rollback()


if __name__ == "__main__":
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            print(etl_bhf_to_eva(conn,'München Hbf'))
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Database error: {error}")
    finally:
        if conn:
            conn.close()

