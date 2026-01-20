'''
Configure test value for pydantic model tests
'''


import pytest

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
