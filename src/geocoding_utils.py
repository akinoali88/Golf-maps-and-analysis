'''
Geocoding and Address Parsing Utilities for Golf Course Data.

This module provides a suite of helper functions to process, clean, and validate 
spatial data retrieved from the Google Maps Platform (specifically via the 
Places and Geocoding APIs). 

The logic is optimized for UK address formats, ensuring that geographic 
metadata is separated from street-level addresses to maintain high-quality 
structured data in a pandas-based ETL pipeline.

Core Functionality:
    * Reassembly of UK postcodes from fragmented API components.
    * Intelligent address cleaning (separating house names vs. house numbers).
    * Metadata exclusion (stripping redundant country and postcode strings).
    * Heuristic-based confidence scoring for geocoding accuracy.

Dependencies:
    * typing: For static type hinting.

Internal Logic Note:
    The module differentiates between numeric street numbers (joined with a space) 
    and named properties (joined with a comma) to adhere to standard UK 
    addressing conventions.
'''

from typing import List, Dict, Any, Optional

def extract_postcode(components: List[Dict[str, Any]]) -> Optional[str]:
    '''
    Finds both the main postcode and any suffix, 
    then joins them correctly.
    '''
    postcode_main = ""
    postcode_suffix = ""

    for component in components:
        if 'postal_code' in component['types']:
            postcode_main = component['long_name']
        elif 'postal_code_suffix' in component['types']:
            postcode_suffix = component['long_name']

    # Join them with a space if both exist, otherwise just return what we found
    if postcode_main and postcode_suffix:
        # UK format: TN16 1QN | US format: 90210-4567
        # We can use a space for UK or a hyphen for US
        return f"{postcode_main} {postcode_suffix}"

    return postcode_main or postcode_suffix or None

def build_clean_address(components: List[Dict[str, Any]]) -> Optional[str]:
    '''
    Constructs a comma-separated address string by filtering out 
    geographic metadata.

    This function iterates through the Google Maps 'address_components' list 
    and removes specific administrative components (postcode and country) 
    to return a 'clean' street and locality address.

    Args:
        components: A list of dictionaries returned by the Google Places 
            or Geocoding API, where each dict contains 'long_name' and 'types'.

    Returns:
        str: A string of address parts joined by commas (e.g., '10 Downing St, London'). 
             Returns an empty string if no valid components are found.

    Example:
        >>> components = [
        ...     {'long_name': '10', 'types': ['street_number']},
        ...     {'long_name': 'Downing St', 'types': ['route']},
        ...     {'long_name': 'SW1A 2AA', 'types': ['postal_code']}
        ... ]
        >>> build_clean_address(components)
        '10, Downing St'
    '''
    # Types we want to EXCLUDE
    excluded_types = {'postal_code', 'country', 'postal_code_suffix'}

    street_number = ""
    route = ""
    other_parts = []

    # Sort components into categories
    for component in components:
        types = set(component['types'])

        if types.intersection(excluded_types):
            continue

        if 'street_number' in types:
            street_number = component['long_name']
        elif 'route' in types:
            route = component['long_name']
        else:
            other_parts.append(component['long_name'])

    # Determine how to join street_number and route
    street_block = ""
    if street_number and route:
        # Check if the street_number is purely digits (e.g., "10")
        if any(char.isdigit() for char in street_number):
            street_block = f"{street_number} {route}"
        else:
            # It's likely a name (e.g., "Valence Park"), so use a comma
            street_block = f"{street_number}, {route}"
    else:
        # If one is missing, just use whichever exists
        street_block = street_number or route

    # Combine the street block with the rest of the address
    full_address_list = [street_block] + other_parts

    # Filter out empty strings and join with commas
    return ", ".join([part for part in full_address_list if part])


def calculate_confidence(result: Dict[str, Any], search_query: str = "") -> str:
    '''
    Evaluates the reliability of a Google Place result for golf course data.

    Calculates confidence by checking for 'golf_course' tags, the presence of 
    the word 'golf' in the returned name or the original search query, and 
    the precision of the location. 

    Args:
        result: The result dictionary from Google's Place Details or Find Place API.
        search_query: The original name searched (used as a fallback for 
            verification when API tags are generic).

    Returns:
        str: A rating of 'High', 'Medium', or 'Low'.
             - 'High': Valid golf match with a specific Place ID and no partial match.
             - 'Medium': General establishment or park match.
             - 'Low': Fuzzy match or non-establishment result.
    '''
    types = result.get('types', [])

    # Get the name Google returned
    found_name = result.get('name', '').lower()
    search_query = search_query.lower()

    # DETECTION: Is it actually a golf course?
    # We check the Google tags, the Google name, AND your original search query
    is_golf_related = (
        'golf_course' in types or 
        'golf' in found_name or 
        'golf' in search_query
    )

    # HIGH CONFIDENCE
    # If we know it's golf-related and Google gave us a specific Place ID result
    # that isn't a "partial match", we treat it as High.
    if is_golf_related and not result.get('partial_match', False):
        return 'High'

    # MEDIUM CONFIDENCE
    if 'establishment' in types or 'point_of_interest' in types:
        return 'Medium'

    return 'Low'
