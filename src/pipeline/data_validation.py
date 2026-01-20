'''
Data Validation Module
----------------------
This module contains the functional logic for validating raw golf course data
using Pydantic models. It separates valid records from invalid ones, providing
a clean dataset for the dashboard and a detailed error log for debugging.
'''

import pandas as pd

from pydantic import ValidationError
from src.models.model import GolfCourse


def validate_golf_courses(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Validates a DataFrame of golf course data against the GolfCourses Pydantic model.

    Each row of the input DataFrame is checked for type correctness, required fields, 
    and constraint violations (e.g., valid Enums, positive numbers). Valid rows are 
    converted to a clean DataFrame, while invalid rows are captured with specific 
    error details.

    Args:
        df (pd.DataFrame): The raw input data loaded from the source.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing:
            - df_validated: DataFrame of clean records, indexed by the ID column.
            - error_df: DataFrame containing the original failed rows plus 
              'total_errors' and 'error_details' columns.

    Note:
        This function outputs a summary report to the console using ANSI styling
        to highlight validation failures or successes..
    '''

    # Define ANSI codes for bold and reset
    bold = '\033[1m'
    end_bold = '\033[0m'

    valid_records = []
    error_records = []

    # Validate each row using Pydantic models
    for record_dict in df.to_dict('records'):
        try:
            # The Pydantic model validates the row data during instantiation
            record = GolfCourse(**record_dict)

            # ensures enum values serialized to str by using json mode
            valid_records.append(record.model_dump(mode='json'))

        except ValidationError as e:

            # Format the message for a single error, separated by new lines
            details = "\n".join(
                f"{i}) {err['loc'][0]}: {err['msg']}"
                for i, err in enumerate(e.errors(), 1)
                )

            # 2. Add one single entry to the error list
            error_records.append({
                **record_dict,
                'total_errors': e.error_count(),
                'error_details': details
            })

    df_validated = pd.DataFrame(valid_records)
    df_errors = pd.DataFrame(error_records)

    total_errors = df_errors['total_errors'].sum() if not df_errors.empty else 0

    if total_errors > 0:
        # Determine pluralisation
        input_label = "input has" if total_errors == 1 else "inputs have"

        print(f"✅ {len(df_validated)} / {len(df)} records have passed validation checks. "
              f"\n🚨 {total_errors} {input_label} failed validation of the "
              f"{bold}golf course {end_bold} requirements. "
              "Please investigate further.")

    else:
        print("✅ All rows passed validation successfully of "
                f"{bold}golf course{end_bold} datasets.")

    return df_validated, df_errors
