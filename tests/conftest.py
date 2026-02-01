'''
Configure test value for pydantic model tests
'''


import pytest
import numpy as np
import pandas as pd

# Fixture for validating geocoding utils
@pytest.fixture
def valid_golf_course_data():

    '''
    Create base data to support testing.
    '''

    return {
        "Course Name": "St Andrews Links",
        "Country": "Scotland",
        "Country Code": "GBR",
        "Course Type": "18 hole",
        "Address": "West Sands Road, St Andrews",
        "Post Code": "KY16 9XL",
        "Latitude": 56.343,
        "Longitude": -2.802,
        "Par": 72,
        "Course Index": 73,
        "Slope Rating": 132
    }

# Fixture for golf course data tests
@pytest.fixture
def course_data():
    """Provides a sample dataframe with various edge cases for golf courses."""
    return pd.DataFrame({
        'Course Name': [
            'Augusta', 'Pebble Beach', 'Augusta',  # Duplicate
            None, np.nan,                          # Nulls
            '   ', '',                             # Whitespace/Empty
            'St Andrews'                           # Unique
        ],
        'Location': ['GA', 'CA', 'GA', 'TX', 'FL', 'UK', 'UK', 'Scotland']
    })


# Fixture for golf round data tests
@pytest.fixture
def round_data():
    """Provides sample round data with potential ID collisions."""
    return pd.DataFrame({
        'Round Number': [1, 2, 2, 3], # Duplicate ID
        'Score': [72, 75, 75, 68]     # Identical row for index 1 and 2
    })
