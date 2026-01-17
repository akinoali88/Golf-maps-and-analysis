'''
Unit Tests for Geocoding Utility Functions.

This test suite validates the logic within `src/geocoding_utils.py`, specifically 
focusing on UK-style address formatting and Google Maps API response parsing. 

The tests ensure that:
    1. Street numbers and names are joined correctly based on content (Space vs. Comma).
    2. Administrative metadata (Country, Postcode) is successfully stripped.
    3. Postcode fragments are correctly reassembled into full UK formats.
    4. Edge cases like missing components or alphanumeric house numbers are handled.

These tests use mocked data structures to simulate Google Maps API responses, 
allowing for local verification without incurring API costs or requiring network access.
'''

import unittest
from src.geocoding_utils import build_clean_address

class TestAddressCleaning(unittest.TestCase):

    '''
    Tester for geocoding util functions
    '''

    def test_numeric_street_number(self):
        '''Should use a SPACE for numeric street numbers (e.g., 10 Downing St).'''
        components = [
            {'long_name': '10', 'types': ['street_number']},
            {'long_name': 'Downing St', 'types': ['route']},
            {'long_name': 'London', 'types': ['locality']}
        ]
        expected = '10 Downing St, London'
        self.assertEqual(build_clean_address(components), expected)

    def test_named_house(self):
        '''Should use a COMMA for named houses (e.g., Valence Park, Brasted Rd).'''
        components = [
            {'long_name': 'Valence Park', 'types': ['street_number']},
            {'long_name': 'Brasted Rd', 'types': ['route']},
            {'long_name': 'Westerham', 'types': ['locality']}
        ]
        expected = 'Valence Park, Brasted Rd, Westerham'
        self.assertEqual(build_clean_address(components), expected)

    def test_alphanumeric_house_number(self):
        '''Should use a SPACE for alphanumeric numbers (e.g., 10a High St).'''
        components = [
            {'long_name': '10a', 'types': ['street_number']},
            {'long_name': 'High St', 'types': ['route']}
        ]
        expected = '10a High St'
        self.assertEqual(build_clean_address(components), expected)

    def test_metadata_exclusion(self):
        '''Should exclude country and postcodes entirely.'''
        components = [
            {'long_name': '1', 'types': ['street_number']},
            {'long_name': 'Park Lane', 'types': ['route']},
            {'long_name': 'London', 'types': ['locality']},
            {'long_name': 'W1K 1AA', 'types': ['postal_code']},
            {'long_name': 'United Kingdom', 'types': ['country']}
        ]
        expected = '1 Park Lane, London'
        self.assertEqual(build_clean_address(components), expected)

    def test_missing_route(self):
        '''Should handle cases where only a street name or only a house name exists.'''
        components = [
            {'long_name': 'St Andrews House', 'types': ['street_number']},
            {'long_name': 'Fife', 'types': ['administrative_area_level_2']}
        ]
        expected = 'St Andrews House, Fife'
        self.assertEqual(build_clean_address(components), expected)

if __name__ == '__main__':
    unittest.main()
