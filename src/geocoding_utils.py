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


def calculate_confidence(result: Dict[str, Any],
                         search_query: str = "",
                         target_types: List[str] = None,
                         keyword: str = "" ) -> str:
    '''
    Evaluates the reliability of a Google Place result against specific activity criteria.

    This function determines 'trustworthiness' by cross-referencing the API's 
    categorical 'types' and the returned 'name' against user-defined targets. 
    It is designed to be activity-agnostic, allowing for validation of golf 
    courses, tennis clubs, or any other specific category.

    Args:
        result: The dictionary returned by the Google Places API (Find Place or Details).
        search_query: The original string used to perform the search.
        target_types: A list of Google 'types' that signal a direct match 
            (e.g., ['golf_course'] or ['spa']).
        keyword: A specific activity string to validate against the returned name 
            (e.g., 'golf' or 'tennis').

    Returns:
        str: A confidence rating:
            - 'High': Matches target types/keyword and is not a partial match.
            - 'Medium': Identified as a general establishment or POI, but lacks 
              specific activity confirmation.
            - 'Low': Flagged as a partial/fuzzy match or lacks required metadata.
    
    '''
    types = result.get('types', [])
    found_name = result.get('name', '').lower()
    search_query = search_query.lower()
    keyword = keyword.lower()

    # Defaults to empty list if none provided
    target_types = target_types or []

    # DYNAMIC DETECTION:
    # 1. Is one of our target types in the Google 'types' list?
    type_match = any(t in types for t in target_types)

    # 2. Does the keyword appear in the result name or the original search?
    keyword_match = keyword in found_name or keyword in search_query if keyword else False

    is_activity_related = type_match or keyword_match

    # HIGH CONFIDENCE
    # Valid match for the specific activity without partial name matching
    if is_activity_related and not result.get('partial_match', False):
        return 'High'

    # MEDIUM CONFIDENCE
    # Valid establishment, but doesn't specifically hit our target activity tags
    if 'establishment' in types or 'point_of_interest' in types:
        return 'Medium'

    return 'Low'
