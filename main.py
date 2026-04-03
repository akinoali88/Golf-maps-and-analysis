"""
Main orchestration page
"""

import os
from dotenv import load_dotenv

from src.pipeline.data_handler import load_source_data
from src.pipeline.data_processing import process_golf_courses, process_golf_rounds
from src.pipeline.data_transformation import generate_course_summaries, transform_round_summaries
from src.pipeline.data_validation import validate_data
from src.pipeline.geocoding import enrich_golf_course_addresses
from src.models.model import GolfCourse, GolfRounds, RoundPerformance
from src.app.app_factory import create_dash_app


# Get google maps API keu
load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

if not api_key:
    raise ValueError("API Key not found! Make sure your .env file is set up correctly.")

# Step 1: Load, process and validate Golf Course Data
golf_courses = load_source_data(file_name="golf rounds.xlsx",
                                excel_params={
                                    "engine": "calamine",
                                    "sheet_name": "golf courses",
                                    "skiprows": 3,
                                    "usecols": "B:M",
                                    "dtype": {"Post Code": str},
                                            })

gc_df = process_golf_courses(golf_courses)

enriched_gc_df = enrich_golf_course_addresses(
    df=gc_df,
    api_key=api_key,
    )

validated_gc_df, gc_errors = validate_data(enriched_gc_df, GolfCourse)

# Step 2: Load, process and validate golf rounds data
golf_rounds = load_source_data(file_name="golf rounds.xlsx",
                                excel_params={
                                    "engine": "calamine",
                                    "sheet_name": "Rounds",
                                    "skiprows": 2,
                                    "usecols": "B:AG",
                                            })


gr_df_processed = process_golf_rounds(golf_rounds)
validated_gr_df, errors = validate_data(
    df=gr_df_processed,
    basemodel= GolfRounds,
    )

# Step 3: process and validate performance data
validated_performance_df, performance_errors = validate_data(
    df=gr_df_processed,
    basemodel=RoundPerformance,
    )

# Step 4: Prepare output metrics
round_summaries = transform_round_summaries(validated_gr_df, validated_gc_df)
course_summaries = generate_course_summaries(round_summaries, validated_gc_df)

# Step 4: Create Dash app
app = create_dash_app(course_summaries, round_summaries)
app.run(debug=True, use_reloader=False, port=8052)
