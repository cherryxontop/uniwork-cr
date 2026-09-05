from bus_journey import time_journey


#set of stops
STOPS = [
    (1, -35.00, 149.00, 'Stop A'),
    (2, -35.00, 149.10, 'Stop B'),
    (3, -35.00, 149.20, 'Stop C'),
    (4, -35.00, 149.30, 'Stop D'),
]


#set of routes
ROUTES = [
    ('1 Loop', [1, 2, 3]),
    ('2 Cross', [2, 4]),
]


#times for each bus trip
DEPARTURES = [
    ('1 Loop', 1, '08:00'), ('1 Loop', 1, '08:30'),
    ('1 Loop', 2, '08:10'), ('1 Loop', 2, '08:40'),
    ('1 Loop', 3, '08:25'), ('1 Loop', 3, '08:55'),

    ('2 Cross', 2, '08:20'), ('2 Cross', 2, '08:50'),
    ('2 Cross', 4, '08:35'), ('2 Cross', 4, '09:05'),
]


#which trip each time belongs to
TRIP_NUMBERS = [
    0, 1,
    0, 1,
    0, 1,
    0, 1,
    0, 1,
]


TIMES = (DEPARTURES, TRIP_NUMBERS)


#empty journey should take 0 minutes
def test_empty_journey():
    journey = []
    assert time_journey(journey, STOPS, ROUTES, TIMES) == 0


#one bus from A to B
def test_single_leg():
    journey = [('1 Loop', 'Stop A', 'Stop B')]
    assert time_journey(journey, STOPS, ROUTES, TIMES) == 10


#one bus from B to C
def test_later_stops():
    journey = [('1 Loop', 'Stop B', 'Stop C')]
    assert time_journey(journey, STOPS, ROUTES, TIMES) == 15


#change buses at Stop B
def test_connection():
    journey = [
        ('1 Loop', 'Stop A', 'Stop B'),
        ('2 Cross', 'Stop B', 'Stop D')
    ]
    assert time_journey(journey, STOPS, ROUTES, TIMES) == 35


#the first connecting bus has already left
def test_later_connection():
    journey = [
        ('1 Loop', 'Stop B', 'Stop C'),
        ('2 Cross', 'Stop B', 'Stop D')
    ]
    assert time_journey(journey, STOPS, ROUTES, TIMES) == 55


#route does not exist
def test_no_route():
    journey = [('99 Nowhere', 'Stop A', 'Stop B')]
    assert time_journey(journey, STOPS, ROUTES, TIMES) is None


# stop does not exist
def test_unknown_stop():
    journey = [('1 Loop', 'Stop A', 'Stop X')]
    assert time_journey(journey, STOPS, ROUTES, TIMES) is None


#no timetable information for the journey
def test_no_times():
    journey = [('1 Loop', 'Stop A', 'Stop B')]
    empty_times = ([], [])
    assert time_journey(journey, STOPS, ROUTES, empty_times) is None


def ran_all_tests():
    test_empty_journey()
    print("test_empty_journey passed")

    test_single_leg()
    print("test_single_leg passed")

    test_later_stops()
    print("test_later_stops passed")

    test_connection()
    print("test_connection passed")

    test_later_connection()
    print("test_later_connection passed")

    test_no_route()
    print("test_no_route passed")

    test_unknown_stop()
    print("test_unknown_stop passed")

    test_no_times()
    print("test_no_times passed")

    print("All tests passed!")


if __name__ == '__main__':
    ran_all_tests()
