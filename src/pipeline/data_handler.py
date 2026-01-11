''' 
Module: data_handler.py

This module provides utility functions for the ingestion and exportation of 
Excel-based datasets. It handles directory management, file existence 
validation, and robust error handling for common I/O issues such as 
permission errors or missing folders.

Functions:
    - load_source_data: Reads Excel files into a pandas DataFrame.
    - export_data: Saves a DataFrame to Excel with automated folder creation.
'''

from pathlib import Path
import pandas as pd

def load_source_data(file_name: str,
                     input_dir_path: str = 'data',
                     excel_params: dict = None) -> pd.DataFrame:

    '''
    Loads raw data from an Excel file into a pandas DataFrame.

    This function serves as the 'Load' step in the ETL pipeline. It constructs 
     the file path and verifies existence.

    Args:
        file_name (str): The name of the file to load (including extension).
        input_dir_path (str, optional): The directory where the file is stored. 
            Defaults to 'data'.
        excel_params (dict, optional): Additional keyword arguments to pass to 
            `pd.read_excel`. If None, defaults to parsing 'Start' and 'Finish' 
            columns as dates.

    Returns:
        pd.DataFrame: A DataFrame containing the raw golf course records.

    Raises:
        FileNotFoundError: If the file does not exist at the constructed path.
        ValueError: If the file extension is not .xls or .xlsx.

    Example:
        >>> df = load_golf_courses("courses_2023.xlsx", excel_params={'sheet_name': 'UK_Courses'})
    '''

    # If excel_params is None, it becomes {}
    excel_params = excel_params or {}

    full_file_path = Path.cwd() / input_dir_path / file_name

        # Use the stored path attribute
    if not full_file_path.exists():
        raise FileNotFoundError(f"File not found at {full_file_path}")

    # Determine the file type
    suffix = full_file_path.suffix.lower()

    if suffix in ('.xls', '.xlsx'):
        df = pd.read_excel(full_file_path, **excel_params)
    else:
        raise ValueError(f"Unsupported file type: {suffix} at {full_file_path}")

    return df


def export_data(
    df: pd.DataFrame,
    output_file_name: str,
    sheet_name: str,
    output_folder: str = 'reporting'
) -> None:
    '''
    Exports a DataFrame to an Excel file within a specified directory.

    This function ensures the target directory exists, handles common OS 
    permission errors (like when the file is already open), and formats 
    date columns for the export.

    Args:
        df: The pandas DataFrame to be exported.
        output_file_name: The name of the output Excel file (e.g., 'report.xlsx').
        sheet_name: The name to assign to the worksheet.
        output_folder: The sub-folder where the file will be saved. 
            Defaults to 'reporting'.

    Returns:
        None
    '''

    # Convert output_folder string to a Path object relative to CWD
    output_dir = Path.cwd() / output_folder

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"\n❌ Permission Denied: Cannot create folder at {output_dir}.")
        return
    except OSError as e:
        print(f"\n❌ General OS Error creating directory '{output_dir}': {e}")
        return

    output_file = output_dir / output_file_name

    try:
        with pd.ExcelWriter(output_file, datetime_format='dd/mm/yyyy') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Success message
        bold, end_bold = '\033[1m', '\033[0m'
        print(f"\n✅ Export successful for {bold}{sheet_name}{end_bold}:")
        print(f"   Location: {output_file.relative_to(Path.cwd())}")

    except PermissionError:
        print(f"\n❌ Permission Denied: The file '{output_file.name}' is likely open. "
              "Please close it and retry.")
    except (OSError, IOError) as e:
        print(f"\n❌ Failed to export data to {output_file}: {e}")
