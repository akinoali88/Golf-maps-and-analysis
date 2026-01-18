'''
Geocoding Module for Golf Course Data.

This module provides functions to fill missing spatial data (addresses, 
latitudes, and longitudes) using external Geocoding APIs. It is designed
to be the 'Enrich' step of an ETL/ELT pipeline.
'''

import time
import googlemaps
import pandas as pd
from googlemaps.exceptions import ApiError, TransportError
from src.geocoding_utils import extract_postcode, build_clean_address, calculate_confidence


def enrich_golf_course_addresses(
    df: pd.DataFrame,
    api_key: str,
    throttle_threshold: int = 100,
    checkpoint_path: str = 'data/enriched_courses.csv'
) -> pd.DataFrame:

    '''
    Enriches a golf course dataset with spatial data and postcodes via Google Places API.

    This function identifies rows missing address information and performs a two-step 
    lookup: first, it uses 'find_place' to obtain a Place ID; second, it uses 
    'place_details' to extract structured address components including the postcode.

    Args:
        df: The input dataset. Must contain 'Golf Course Name' and 'Address' columns.
            The 'Address' column is used to identify records needing enrichment.
        api_key: A valid Google Maps Platform API key with 'Places API' enabled.
        throttle_threshold: The row count threshold at which a 0.1s delay 
            is activated per request to prevent rate-limit errors.
        checkpoint_path: The file system path where progress is saved every 10 rows.

    Returns:
        pd.DataFrame: The enriched DataFrame with 'Address', 'Latitude', 'Longitude', 
            and 'Postcode' columns updated.

    Raises:
        googlemaps.exceptions.ApiError: If the API key is invalid or quota is exceeded.
        googlemaps.exceptions.TransportError: If a network connection failure occurs.
        KeyError: If the input DataFrame is missing required columns.

    Notes:
        - API Costs: This function performs two API calls per missing address 
          (Find Place + Place Details), which may incur higher costs.
        - Fields: Uses specific 'address_component' fields to retrieve postcodes 
          which are not available in standard string-based searches.

    Implementation Notes:
    * Two-Step Geocoding: We use a 'Find Place' -> 'Place Details' workflow. 
      'Find Place' is used for the initial discovery and precision metadata 
      (location_type), while 'Place Details' is required to fetch granular 
      'address_components' for postcode and street-level parsing.
    
    * Activity Heuristics: Confidence scoring relies on a "Target + Keyword" 
      model. This accommodates cases where Google identifies a location as a 
      generic 'park' or 'establishment' but the name or search query 
      confirms the specific activity (e.g., 'golf').
    
    * API Field Constraints: Field names are intentionally pluralized 
      (e.g., 'address_components', 'types') to align with the latest 
      Google Maps Python Client requirements, ensuring all metadata is 
      returned in the response.
    
    * UK Addressing: The cleaning logic assumes a UK standard. Named properties 
      (without numbers) are treated as distinct components from the street 
      (route) to prevent "Address Line 1" collisions.
          
    '''
    gmaps = googlemaps.Client(key=api_key)

    # Identify rows needing enrichment
    mask = df['Address'].isna() | (df['Address'] == '')
    rows_to_process = mask.sum()

    if rows_to_process == 0:
        print('✅ All golf courses have location data. Skipping geocoding.')
        return df

    print(f"Found {rows_to_process} records to enrich.")

    df = df[mask].copy()

    # Iterate over the original DataFrame using the mask
    for count, (index, row) in enumerate(df.iterrows(), 1):
        course_name = row.get('Golf Course')
        if not course_name:
            continue

        try:
            # STEP 1: Find the Place ID and Basic Geometry
            find_result = gmaps.find_place(
                input=course_name,
                input_type='textquery',
                fields=['place_id', 'formatted_address', 'geometry', 'types']
            )

            if find_result.get('status') == 'OK' and find_result.get('candidates'):
                candidate = find_result['candidates'][0]
                place_id = candidate.get('place_id')

                # Grab the location_type HERE (Step 1)
                # This is where ROOFTOP or GEOMETRIC_CENTER usually lives
                found_loc_type = candidate.get('geometry', {}).get('location_type')

                # Fill basic info from first call
                df.at[index, 'Address'] = candidate.get('formatted_address')
                if 'geometry' in candidate:
                    df.at[index, 'Latitude'] = candidate['geometry']['location']['lat']
                    df.at[index, 'Longitude'] = candidate['geometry']['location']['lng']

                # STEP 2: Get the Postcode using Place Details
                if place_id:
                    # 'address_component' is the field name required by the library
                    details = gmaps.place(
                        place_id=place_id,
                        fields=['address_component', 'geometry', 'type', 'name']
                    )

                    if details.get('status') == 'OK':

                        components = details.get('result', {}).get('address_components', [])

                        full_result = details.get('result', {})

                        # 1. Extract Postcode for your Postcode column
                        df.at[index, 'Post Code'] = extract_postcode(components)

                        # 2. Build the Clean Address (No Postcode/Country)
                        df.at[index, 'Address'] = build_clean_address(components)

                        # 3 Get confidence level of geocode
                        # Inject the location_type from Step 1 into the Step 2 result
                        # This "plugs the hole" so calculate_confidence can see it
                        if found_loc_type:
                            full_result['geometry']['location_type'] = found_loc_type

                        df.at[index, 'Confidence'] = calculate_confidence(
                            full_result,
                            course_name,
                            target_types=['golf_course'],
                            keyword='golf')

            # --- SMART THROTTLE ---
            if rows_to_process > throttle_threshold:
                time.sleep(0.1)

            # --- CHECKPOINTING ---
            if count % 10 == 0:
                df.to_csv(checkpoint_path, index=False)
                print(f"Progress saved: {count}/{rows_to_process} rows processed.")

        except (ApiError, TransportError) as e:
            print(f"Network or API Error for {course_name}: {e}")
            if 'API key' in str(e):
                break


    # Final save after loop finishes
    df.to_csv(checkpoint_path, index=False)
    print(f"Enrichment complete. Final data saved to {checkpoint_path}")
    return df
