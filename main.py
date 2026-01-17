'''
Main orchestration page
'''

import os
from dotenv import load_dotenv
from src.pipeline.data_handler import load_source_data
from src.pipeline.data_pipeline import process_golf_courses
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
                                    'usecols': 'B:H',
                                            })

# Clean Golf Course Data
golf_course = process_golf_courses(golf_courses)

output = enrich_golf_course_addresses(
    df=golf_course,
    api_key=api_key,
    )

print(output)



# Create Dash app
app = create_dash_app()
app.run(debug=True, use_reloader=False, port=8052)
