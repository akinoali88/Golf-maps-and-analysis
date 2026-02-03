'''
Main orchestration page
'''

import os
from dotenv import load_dotenv

from src.pipeline.data_handler import load_source_data
from src.pipeline.data_processing import process_golf_courses, process_golf_rounds
from src.pipeline.data_transformation import generate_course_summaries
from src.pipeline.data_validation import validate_data
from src.pipeline.geocoding import enrich_golf_course_addresses
from src.models.model import GolfCourse, GolfRounds
from src.app.app_factory import create_dash_app


# Get google maps API keu
load_dotenv()
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

if not api_key:
    raise ValueError("API Key not found! Make sure your .env file is set up correctly.")

# Step 1: Load, process and validate Golf Course Data
golf_courses = load_source_data(file_name='golf rounds.xlsx',
                                excel_params={
                                    'engine': 'calamine',
                                    'sheet_name': 'golf courses',
                                    'skiprows': 3,
                                    'usecols': 'B:M',
                                    'dtype': {'Post Code': str},
                                            })

gc_df = process_golf_courses(golf_courses)

enriched_gc_df = enrich_golf_course_addresses(
    df=gc_df,
    api_key=api_key,
    )

validated_gc_df, gc_errors = validate_data(enriched_gc_df, GolfCourse)

# Step 2: Load, process and validate golf rounds data
gr_df = load_source_data(file_name='golf rounds.xlsx',
                                excel_params={
                                    'engine': 'calamine',
                                    'sheet_name': 'Rounds',
                                    'skiprows': 2,
                                    'usecols': 'B:AG',
                                            })


gr_df_processed = process_golf_rounds(gr_df)

validated_gr_df, errors = validate_data(gr_df_processed, GolfRounds)

# Step 3: Load performance data

# Step 4: Prepare output metrics
golf_round_summary = generate_course_summaries(validated_gr_df, validated_gc_df)

# transform golf course data
# to do

# Merge golf rounds with golf course data
# to do

# Create Dash app
app = create_dash_app(golf_round_summary)
app.run(debug=True, use_reloader=False, port=8052)
