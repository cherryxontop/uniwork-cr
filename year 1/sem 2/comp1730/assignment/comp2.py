import csv
import pandas as pd


def load_stops(path='bus_stops.csv'):
    file2 = pd.read_csv(path) #reads csv
    stops = []
    for i in range(len(file2)):
        stop_id = int(file2['id'][i])      #values in the "id" row
        lat = float(file2['lat'][i])       #values in the "lat" column
        lon = float(file2['lon'][i])       #values in the "lon" column
        name = file2['name'][i]            #values in the "name" column
        #converting values to a list
        stops.append((stop_id, lat, lon, name))
    return stops
 
 
def load_routes(path='bus_routes.csv'):
    routes = []
    #opening file using pythons csv reader because im not sure if can pandas can read non-uniform rows
    with open(path, newline='', encoding='utf-8') as file1: #as per documentation
        df1 = csv.reader(file1)
        for row in df1:
            name = row[0]   #first value in the row
            stop_ids = []   
            for value in row[1:]:   #everything after [0] i.e. stops id's
                stop_ids.append(int(value))
            routes.append((name, stop_ids)) #tuple: (name.[id1, id2, id3])
    return routes
 
 
def load_times(path='times.csv'):
    departures = []    #(route, stop_id, time_string): one entry per bus departure
    trip_numbers = []  #which trip of the day each entry in departures[] is
 
    with open(path, newline='', encoding='utf-8') as file2:
        df2 = csv.reader(file2)
        for row in df2:
            route = row[0]
            stop_id = int(row[1])
            trip = 0
            for value in row[2:]:
                departures.append((route, stop_id, value))
                trip_numbers.append(trip)
                trip += 1
 
    return departures, trip_numbers


def print_journey(journey):
    '''
    Prints a bus journey.
    Param journey: a list of (route_name, bus_stop_name_a, bus_stop_name_b) tuples
    The argument should be a valid journey data structure, as
    described in the assignment specification.
    The function does not return a value.
    '''
    print('Start at {}.'.format(journey[0][1]))
    for stop_number, (route, stop_a, stop_b) in enumerate(journey):
        print('{}. Take {} from {} to {}.'.format(
            stop_number + 1, route, stop_a, stop_b))
    print('Arrived at {}.'.format(journey[-1][2]))


# ---------------------------------------------------------------------
# Task 1
# ---------------------------------------------------------------------
 
# approximate coordinates of CSIT
CSIT_LATITUDE = -35.2753
CSIT_LONGITUDE = 149.12056
 
 
def southernmost_stop(stops):
    """name of the stop with the smallest or most negative latitude"""
    best_stop = stops[0]
    for stop in stops:
        if stop[1] < best_stop[1]:
            best_stop = stop
    return best_stop[3]
 
 
def closest_stop_to_csit(stops):
    """name of the stop closest to CSIT"""
    best_stop = stops[0]
    best_distance = (best_stop[1] - CSIT_LATITUDE) ** 2 + (best_stop[2] - CSIT_LONGITUDE) ** 2
 
    for stop in stops:
        distance = (stop[1] - CSIT_LATITUDE) ** 2 + (stop[2] - CSIT_LONGITUDE) ** 2
        if distance < best_distance:
            best_stop = stop
            best_distance = distance
 
    return best_stop[3]
 
 
def most_common_number(routes):
    """the route number used by the most routes"""
    counts = {}
    for name, stop_ids in routes:
        number = name.split(' ', 1)[0]
        if number in counts:
            counts[number] += 1
        else:
            counts[number] = 1
 
    best_number = None
    best_count = 0
    for number in counts:
        if counts[number] > best_count:
            best_number = number
            best_count = counts[number]
 
    return best_number
 
 
def most_stops(routes):
    """name of the route that visits the most bus stops"""
    best_name = routes[0][0]
    best_count = len(routes[0][1])
 
    for name, stop_ids in routes:
        if len(stop_ids) > best_count:
            best_name = name
            best_count = len(stop_ids)
 
    return best_name
 
 
# ---------------------------------------------------------------------
# Task 2
# ---------------------------------------------------------------------
 
def find_route(stops, routes, stop_a, stop_b):
    """A direct (no-transfer) journey from stop_a to stop_b, or [] if none exists."""
    id_a = stop_a[0]
    name_a = stop_a[3]
    id_b = stop_b[0]
    name_b = stop_b[3]
 
    for route_name, stop_ids in routes:
        if id_a in stop_ids and id_b in stop_ids:
            index_a = stop_ids.index(id_a)
            index_b = stop_ids.index(id_b)
            if index_a < index_b:
                return [(route_name, name_a, name_b)]
 
    return []
 
 
# ---------------------------------------------------------------------
# Task 3
# ---------------------------------------------------------------------
 
def _to_minutes(time_str):
    """Convert an 'HH:MM' string into minutes since midnight."""
    hours_str, minutes_str = time_str.split(':')
    return int(hours_str) * 60 + int(minutes_str)
 
 
def time_journey(journey, stops, routes, times):
    """
    Minutes to travel `journey`, assuming you catch the first bus of
    the day for the first leg, then the first bus at/after your
    arrival time for every later leg (so connection waits count, but
    time spent waiting for your very first bus doesn't).
    `times` is the list produced by load_times(). Returns None if any
    leg has no usable timetable data.
    """
    if len(journey) == 0:
        return 0
 
    # Which stop ids belong to which route (used below to work out
    # which stop id a name refers to - some stop names are shared by
    # more than one stop, so we can't just look up a name on its own).
    route_stop_ids = {}
    for name, stop_ids in routes:
        route_stop_ids[name] = stop_ids
 
    start_time = None
    current_time = None
 
    for route, name_a, name_b in journey:
        stop_ids = route_stop_ids.get(route, [])
 
        id_a = None
        for stop_id, lat, lon, name in stops:
            if name == name_a and stop_id in stop_ids:
                id_a = stop_id
                break
 
        id_b = None
        for stop_id, lat, lon, name in stops:
            if name == name_b and stop_id in stop_ids:
                id_b = stop_id
                break
 
        if id_a is None or id_b is None:
            return None
 
        # Find the earliest departure from stop A at/after current_time.
        best_trip = None
        best_departure = None
        for r, stop_id, trip, time_str in times:
            if r == route and stop_id == id_a:
                minutes = _to_minutes(time_str)
                if current_time is None or minutes >= current_time:
                    if best_departure is None or minutes < best_departure:
                        best_departure = minutes
                        best_trip = trip
 
        if best_trip is None:
            return None
 
        # Find when that same trip arrives at stop B.
        arrival_time = None
        for r, stop_id, trip, time_str in times:
            if r == route and stop_id == id_b and trip == best_trip:
                arrival_time = _to_minutes(time_str)
                break
 
        if arrival_time is None:
            return None
 
        if start_time is None:
            start_time = best_departure
        current_time = arrival_time
 
    return current_time - start_time
 
 
if __name__ == '__main__':
    pass
 