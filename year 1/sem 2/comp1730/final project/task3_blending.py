"""
task3_blending.py

Task 3 - Improve the quality of a single wine through blending it with one 
or more wines from a list of candidates and their physiochemical properties.

Required function:

choose_candidates()

Please choose wines for testing this program from the 
winequality_red_260818_TEST.csv file only!
"""

import winequality

# Source of input and candidate wines to test this program:
TEST_FILE = "winequality_red_260918_TEST.csv"

def choose_candidates(primary, candidates, model):
    """
    Find which candidate wine blends with your primary wine will 
    give the best quality.

    primary - physiochemical properties of the wine from your estate
    candidates - list of wines to consider, taken from TEST_FILE

    Returns the winning blend, along with the candidates and ratios used.
    """
    pass


if __name__ == "__main__":
    model = winequality.build_model()
    primary = dict()
    candidates = list()
    choose_from_candidates(primary, candidates, model)
