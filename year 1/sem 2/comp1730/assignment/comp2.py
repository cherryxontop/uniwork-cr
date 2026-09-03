import csv
import numpy as np
import pandas as pd


def load_stops(path='bus_stops.csv'):
    file2 = pd.read_csv(path) #reads csv
    stops = []
    for i in range(len(file2)):
        stop_id = int(file2['id'][i]) #values in the "id" column
        lat = float(file2['lat'][i]) #values in the "lat" column
        lon = float(file2['lon'][i]) #values in the "lon" column
        name = file2['name'][i] #values in the "name" column
        #converting values to a list
        stops.append((stop_id, lat, lon, name))
    return stops
 
 
def load_routes(path='bus_routes.csv'):
    routes = []
    # opening the file using Python's csv reader
    with open(path, newline='', encoding='utf-8') as file1:
        df1 = csv.reader(file1)
        for row in df1:
            name = row[0] # first value in the row
            stop_ids = []
            for value in row[1:]: # everything after the route name
                stop_ids.append(int(value))
            routes.append((name, stop_ids)) # tuple: (name, [id1, id2, id3])
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


# task 1
 
# approximate coordinates of CSIT
CSIT_LATITUDE = -35.2753
CSIT_LONGITUDE = 149.12056
 
 
def southernmost_stop(stops):
    """name of the stop with the smallest or most negative latitude."""
    best_stop = min(stops, key=lambda s: s[1]) #filters thru the latitudes in the stop tuples to find the minimum value.
    return best_stop[3]     #returns the 3rd index which is the name of the stop


def closest_stop_to_csit(stops):
    """
    name of the stop closest to CSIT
    using pythagoras's theorem (a^2 + b^2 = c^2) to calculate 
    the straight-line distance between each bus stop and the CSIT building:
    - a represents the difference in longitudes (horizontal distance).
    - b represents the difference in latitudes (vertical distance).
    - c represents the straight-line distance.
    """
    def distance(stop):
        a = (stop[1] - CSIT_LATITUDE)
        b = (stop[2] - CSIT_LONGITUDE)
        c = np.sqrt(a**2 + b**2)
        return c
    
    best_stop = min(stops, key=distance) #filters thru the latitudes in the stop tuples to find the minimum value.
    return best_stop[3] #returns the 3rd index which is the name of the stop


def most_common_number(routes):
    """the route number used by the most routes"""
    counts = {}
    for name, stop_ids in routes:
        number = name.split(' ', 1)[0] # take the first word of the name, e.g. '10'
        if number in counts: # have we seen this number before?
            counts[number] += 1 # yes -> add one to its count
        else:
            counts[number] = 1 # no -> start its count at one
 
    best_number = None 
    best_count = 0  # so the highest count so far is zero
    for number in counts: # look at every number we counted
        if counts[number] > best_count: # does this number beat the current winner?
            best_number = number # yes -> it's our new winner
            best_count = counts[number] # ...and remember its count too
 
    return best_number # return the number with the highest count


def most_stops(routes):
    """name of the route that visits the most bus stops"""
    best_name = routes[0][0] # name of the first route (starting guess)
    best_count = len(routes[0][1]) # how many stops that first route has
 
    for name, stop_ids in routes: # check every route
        if len(stop_ids) > best_count: # does this route have more stops?
            best_name = name # yes -> it's our new best guess
            best_count = len(stop_ids) # ...and remember its stop count too
 
    return best_name # return the name of the winner


# task 2

def find_route(stops, routes, stop_a, stop_b):
    """direct journey from stop_a to stop_b"""
    id_a = stop_a[0] # id of the stop we're starting at
    name_a = stop_a[3] # name of the stop we're starting at
    id_b = stop_b[0] # id of the stop we want to reach
    name_b = stop_b[3] # name of the stop we want to reach
 
    for route_name, stop_ids in routes:
        if id_a in stop_ids and id_b in stop_ids:  # does this route visit both stops?
            index_a = stop_ids.index(id_a) # where stop_a sits in the route's stop order
            index_b = stop_ids.index(id_b) # where stop_b sits in the route's stop order
            if index_a < index_b: # does the route reach stop_a before stop_b?
                return [(route_name, name_a, name_b)]  # yes -> return a one-leg journey
 
    return [] # no route goes directly from a to b


# task 3

def _to_minutes(time):
    hours, minutes = time.split(':') # split the time into hours and minutes
    return int(hours) * 60 + int(minutes) # convert everything into minutes

def time_journey(journey, stops, routes, times):
    departures, trip_numbers = times # get the two lists from load_times()
    if not journey: # if there is no journey
        return 0

    current_time = None # arrival time at the current stop
    start_time = None # time we catch the first bus

    for route, stop_a, stop_b in journey: # go through each leg of the journey
        # find the stop IDs belonging to this route
        stop_ids = []

        for name, ids in routes:
            if name == route:
                stop_ids = ids
                break
        id_a = None # ID of the starting stop
        id_b = None # ID of the destination stop

        for stop_id, lat, lon, name in stops: # search through all stops
            if name == stop_a and stop_id in stop_ids:
                id_a = stop_id # found stop A
            if name == stop_b and stop_id in stop_ids:
                id_b = stop_id # found stop B
        if id_a is None or id_b is None: # if either stop could not be found
            return None

        # find departure times for stop A
        times_a = []
        for i in range(len(departures)):
            if departures[i][0] == route and departures[i][1] == id_a:
                times_a.append((departures[i][2], trip_numbers[i]))

        # find arrival times for stop B
        times_b = []
        for i in range(len(departures)):
            if departures[i][0] == route and departures[i][1] == id_b:
                times_b.append((departures[i][2], trip_numbers[i]))

        if not times_a or not times_b: # if there is no timetable data
            return None

        # find the first bus we can catch
        for departure, trip in times_a:
            departure_time = _to_minutes(departure)
            if current_time is None or departure_time >= current_time:
                # find the same bus at stop B
                for arrival, arrival_trip in times_b:
                    if arrival_trip == trip:
                        arrival_time = _to_minutes(arrival)
                        if start_time is None: # first leg of the journey
                            start_time = departure_time
                        current_time = arrival_time
                        break
                else:
                    return None
                break
        else:
            return None # no suitable bus was found
    return current_time - start_time # total journey time in minutes