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

    data_list = []
    errors = []

    # Validate each row using Pydantic models
    for _, row in df.iterrows():
        try:
            # The Pydantic model validates the row data during instantiation
            record = GolfCourse(**row.to_dict())

            # ensures enum values serialized to str by using json mode
            data_list.append(record.model_dump(mode='json'))

        except ValidationError as e:

            # Collect error details for each invalid row
            output_errors = []

            # Accessing individual elements of the error dictionary
            for i, error in enumerate(e.errors(), 1):

                # Format the message for a single error, separated by new lines
                output_error = f"{i}) {error['input']}: {error['msg']}"
                output_errors.append(output_error)
                error_details = ".\n".join(output_errors)

                error_row = {**row.to_dict(),   # include original data for reference
                            'total_errors': e.error_count(),
                            'error_details': error_details}

                errors.append(error_row)

    # Create DataFrame for valid records
    df_validated = pd.DataFrame(data_list)

    # Create DataFrame for error records
    col_names = df.columns.tolist()
    col_names += ['total_errors', 'error_details']

    error_df = pd.DataFrame(errors,
                            columns=col_names)

    # --- Summary Report at the End ---
    total_errors = error_df['total_errors'].sum()

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

    return df_validated, error_df
