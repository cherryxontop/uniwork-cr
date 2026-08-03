## COMP1730/6730 Homework Assignment 1

"""
ANU ID: u8336188
NAME: Chhaya Gopal Ramnani

By inputting my UID and name, I declare that this submission is my own work.
I am able to explain and justify all parts of this submission if asked.
https://www.anu.edu.au/students/academic-skills/academic-integrity
"""
def estimate_race_time(time_25km, windy, hot):
    pass

def estimate_race_time_refined(time_25km, wind_level, temperature_c):
    pass

def simulate_training_block(time_25km):
    pass

################################################################################
#               DO NOT MODIFY THE TEST FUNCTION
# The testing functions below are provided if you want to test your code
# in your favourite IDE instead of using the Ed platform. They run the
# same set of test cases as when you click the "Test" button on Ed website
################################################################################

def test_estimate_race_time_cases():
    assert abs(estimate_race_time(30.0, False, False) - 129.6) < 1e-4
    assert abs(estimate_race_time(0.0, True, True) - 0.0) < 1e-4
    assert abs(estimate_race_time(25, False, True) - 112.0) < 1e-4
    assert abs(estimate_race_time(100.0, True, True) - 468.0) < 1e-4
    assert abs(estimate_race_time(30.0, True, False) - 135.6) < 1e-4

def test_estimate_race_time_refined_cases():
    assert abs(estimate_race_time_refined(30.0, "no wind", 15) - 129.6) < 1e-4
    assert abs(estimate_race_time_refined(30.0, "moderate wind", 15) - 135.6) < 1e-4
    assert abs(estimate_race_time_refined(30.0, "very windy", 15) - 141.6) < 1e-4
    assert abs(estimate_race_time_refined(28.5, "moderate wind", 22) - 132.24) < 1e-4
    assert abs(estimate_race_time_refined(50.78125, "moderate wind", 22) - 235.625) < 1e-4
    

def test_simulate_training_block_cases():
    assert abs(simulate_training_block(35.0) - 499.8) < 1e-4
    assert abs(simulate_training_block(55.0) - 255.2) < 1e-4
    assert abs(simulate_training_block(20.0) - 285.6) < 1e-4
    assert abs(simulate_training_block(40.0) - 571.2) < 1e-4
    assert abs(simulate_training_block(65.0) - 0.0) < 1e-4


def test_assignment1():
    test_estimate_race_time_cases()
    test_estimate_race_time_refined_cases()
    test_simulate_training_block_cases()
    print("all non-hidden tests passed")