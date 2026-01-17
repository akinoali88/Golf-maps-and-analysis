''' Module for processing data files including loading, cleaning, and validating.
Steps orchestrated within the DataProcessor class.
'''

import pandas as pd


def process_golf_courses(df: pd.DataFrame,
                         col_name: str = 'Golf Course Name') -> pd.DataFrame:

    '''
    Cleans the DataFrame by removing invalid entries and redundant golf course records.

    This function performs a two-stage cleanup:
    1. Row Filtering: Removes any records where the specified column is null, 
       NaN, or consists solely of whitespace/empty strings.
    2. Deduplication: Identifies and removes duplicate course names, keeping only 
       the first occurrence encountered.

    Args:
        df (pd.DataFrame): The input DataFrame containing golf course data.
        col_name (str): The name of the column to validate and deduplicate. 
            Defaults to 'Golf Course Name'.

    Returns:
        pd.DataFrame: A cleaned copy of the original DataFrame with missing values 
            and duplicates removed.

    Notes:
        - The function prints a summary of removed rows and a list of specific 
          duplicated courses to the console for audit purposes.
        - The returned DataFrame is a deep copy to prevent 'SettingWithCopy' warnings.
    '''

    # 1. Remove rows with no golf course name
    initial_count = len(df)

    # Drop actual NaN/None values
    df = df.dropna(subset=[col_name]).copy()

    # Drop rows that are just empty strings or whitespace
    df = df[df[col_name].astype(str).str.strip() != ""]

    rows_removed = initial_count - len(df)
    if rows_removed > 0:
        print(f"Removed {rows_removed} rows with missing Golf Course Names.")
    else:
        print("No missing names found.")


    # 2. Identify duplicate golf course entiries and remove
    duplicate_mask = df.duplicated(subset=[col_name], keep='first')
    duplicate_list = df.loc[duplicate_mask, col_name].unique().tolist()

    # Print duplicate golf courses
    if duplicate_list:
        print("⚠️--- Duplicate Detection ---")
        print(f"Found {len(duplicate_list)} duplicate entries.")
        print(f"These are the duplicate courses: {', '.join(duplicate_list)}")
    else:
        print("✅ No duplicate courses in dataset\n")

    # Drop the duplicates and return the clean DataFrame
    df_cleaned = df.drop_duplicates(subset=[col_name], keep='first').copy()

    return df_cleaned
