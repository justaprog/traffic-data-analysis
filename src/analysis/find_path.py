

# Planned Path. A sequence of station names separated by the pipe symbols ('|').
# E.g.: 'Mainz Hbf|R sselsheim|Frankfrt(M) Flughafen'.

# For arrival, the path indicates the stations that come before the current station. 
# The first element then is the trip's start station.

# For departure, the path indicates the stations that come after the current station. 
# The last element in the path then is the trip's destination station.
# Note that the current station is never included in the path (neither for arrival nor for departure).
def find_path(des, arr):
    duration = 0
    path = []
    return path,duration