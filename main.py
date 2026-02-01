'''
Main orchestration page
'''

import os
from dotenv import load_dotenv

from src.pipeline.data_handler import load_source_data
from src.pipeline.data_processing import process_golf_courses, process_golf_rounds
from src.models.model import GolfCourse, GolfRounds
from src.pipeline.data_validation import validate_data
from src.pipeline.geocoding import enrich_golf_course_addresses
from src.pipeline.data_aggregation import generate_course_summaries
# from src.app.app_factory import create_dash_app


# Get google maps API keu
load_dotenv()
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

if not api_key:
    raise ValueError("API Key not found! Make sure your .env file is set up correctly.")

# Step 1: Get Golf Course Data
golf_courses = load_source_data(file_name='golf rounds.xlsx',
                                excel_params={
                                    'engine': 'calamine',
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

validated_gc_df, gc_errors = validate_data(enriched_gc_df, GolfCourse)

# Step 2: Get Golf Round Data

gr_df = load_source_data(file_name='golf rounds.xlsx',
                                excel_params={
                                    'engine': 'calamine',
                                    'sheet_name': 'Rounds',
                                    'skiprows': 2,
                                    'usecols': 'B:AG',
                                            })


gr_df_processed = process_golf_rounds(gr_df)

validated_gr_df, errors = validate_data(gr_df_processed, GolfRounds)

golf_rounds = generate_course_summaries(validated_gr_df, validated_gc_df)

print(golf_rounds)


# transform golf course data
# to do

# Merge golf rounds with golf course data
# to do

# Create Dash app
# app = create_dash_app(validated_gc_df)
# app.run(debug=True, use_reloader=False, port=8052)
