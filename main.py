'''
Main orchestration page
'''

import os
from dotenv import load_dotenv
from src.pipeline.data_handler import load_source_data
from src.pipeline.data_pipeline import process_golf_courses
from src.pipeline.data_validation import validate_golf_courses
from src.pipeline.geocoding import enrich_golf_course_addresses
from src.app.app_factory import create_dash_app


# This looks for the .env file and loads the variables into your environment
load_dotenv()

# Now you can access it like a regular environment variable
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

if not api_key:
    raise ValueError("API Key not found! Make sure your .env file is set up correctly.")

golf_courses = load_source_data(file_name='golf rounds.xlsx',
                                excel_params={
                                    'sheet_name': 'golf courses',
                                    'skiprows': 3,
                                    'usecols': 'B:M',
                                    'dtype': {'Post Code': str},
                                            })

# Clean Golf Course Data
gc_df = process_golf_courses(golf_courses)

enriched_gc_df = enrich_golf_course_addresses(
    df=gc_df,
    api_key=api_key,
    )

validated_gc_df, validation_errors = validate_golf_courses(enriched_gc_df)

if len(validation_errors) > 0:
    print(validation_errors)

# Create Dash app
# app = create_dash_app(validated_gc_df)
# app.run(debug=True, use_reloader=False, port=8052)
