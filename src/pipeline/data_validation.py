"""
Data Validation Module
----------------------
This module contains the functional logic for validating raw golf data
using Pydantic models. It separates valid records from invalid ones, providing
a clean dataset for the dashboard and a detailed error log for debugging.
"""

from typing import Tuple, Type, TypeVar, get_args, get_origin, Union
from datetime import date, datetime
import pandas as pd
from pydantic import BaseModel, ValidationError

from src.pipeline.data_handler import export_data

# T allows us to return the specific model type used
T = TypeVar("T", bound=BaseModel)

def validate_data(df: pd.DataFrame,
                  basemodel: Type[T]
                  ) -> Tuple[pd.DataFrame, pd.DataFrame]:

    """
    Validates a DataFrame of golf course data against the a define Pydantic BaseModel.

    Each row of the input DataFrame is checked for type correctness, required fields, 
    and constraint violations (e.g., valid Enums, positive numbers). Valid rows are 
    converted to a clean DataFrame, while invalid rows are captured with specific 
    error details.

    Args:
        df (pd.DataFrame): The raw input data loaded from the source.
        basemodel (Type[T]): A Pydantic BaseModel class that defines the expected schema
            structure, field types, and validation rules for the data.

    Returns:
        Tuple:
            - df_validated (pd.DataFrame): DataFrame of clean records, indexed by the ID column.
            - error_df (pd.DataFrame): DataFrame containing the original failed rows plus 
            "total_errors" and "error_details" columns.

    Note:
        This function outputs a summary report to the console using ANSI styling
        to highlight validation failures or successes..
    """

    # Define ANSI codes for bold and reset
    bold = "\033[1m"
    end_bold = "\033[0m"

    valid_records = []
    error_records = []

    # Validate each row using Pydantic models
    for record_dict in df.to_dict("records"):
        try:
            # The Pydantic model validates the row data during instantiation
            record = basemodel(**record_dict)

            # ensures enum values serialized to str by using json mode
            valid_records.append(record.model_dump(mode="json"))

        except ValidationError as e:

            # Format the message for a single error, separated by new lines
            details = "\n".join(
                f"{i}) {err['loc'][0]}: {err['msg']}"
                for i, err in enumerate(e.errors(), 1)
                )

            # 2. Add one single entry to the error list
            error_records.append({
                **record_dict,
                "total_errors": e.error_count(),
                "error_details": details
            })


    df_validated = pd.DataFrame(valid_records)

    # ensure all dates are in datetime format for downstream processing
    if not df_validated.empty:

        for field_name, field_info in basemodel.model_fields.items():

            # Get the type hint (e.g., date, datetime, or Optional[date])
            annotation = field_info.annotation

            # 2. Handle Optional/Union types (e.g., Optional[date] is Union[date, None])
            origin = get_origin(annotation)
            if origin is Union:
                types = get_args(annotation)
            else:
                types = (annotation,)

            if any(t in (date, datetime) for t in types):
                if field_name in df_validated.columns:
                    df_validated[field_name] = pd.to_datetime(df_validated[field_name])

    df_errors = pd.DataFrame(error_records)

    total_errors = df_errors["total_errors"].sum() if not df_errors.empty else 0

    if total_errors > 0:
        # Determine pluralisation
        input_label = "input has" if total_errors == 1 else "inputs have"

        export_file_name = f"{basemodel.label}_validation_errors.xlsx"

        print(f"✅ {len(df_validated)} / {len(df)} records have passed validation checks. "
              f"\n🚨 {total_errors} {input_label} failed validation of the "
              f"{bold}{basemodel.label}{end_bold} requirements. "
              "Please investigate further.")

        export_data(df_errors, export_file_name, "errors")

        print("❗ Validation errors exported to "
              f"{bold}reporting/{export_file_name}{end_bold} file.")


    else:
        print("✅ All rows passed validation successfully of "
                f"{bold}{basemodel.label}{end_bold} datasets.")

    return df_validated, df_errors
