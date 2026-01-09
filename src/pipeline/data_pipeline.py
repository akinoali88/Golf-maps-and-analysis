''' Module for processing data files including loading, cleaning, and validating.
Steps orchestrated within the DataProcessor class.
'''

from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from models.model import Data

class DataPipeline:
    '''
    Class for loading, cleaning, validating and processing data.
    '''

    # 1. DEFINE CONSTANTS AS CLASS ATTRIBUTES
    # Define ANSI codes for bold and reset
    bold = '\033[1m'
    end_bold = '\033[0m'

    def __init__(self,
                 file_name: str,
                 input_dir_path: str = 'data',
                 excel_params: dict = None):

        '''
        Initializes the DataProcessor with configuration.
        '''

        self.file_name = file_name
        self.input_dir_path = input_dir_path

        # Initialize blank dataframes to be updated during processing
        self.raw_data: pd.DataFrame = None
        self.validated_data : pd.DataFrame = None
        self.transformed_data : pd.DataFrame = None
        self.input_data_errors: pd.DataFrame = None

        # Define default excel parameters if none are provided
        self.excel_params = excel_params if excel_params is not None else {
            'parse_dates': ['Start', 'Finish']}

        # Calculate and store the absolute file path once
        # Using Path.cwd() assumes 'input_dir_path' is relative to the script's execution location.
        self.full_file_path = Path.cwd() / input_dir_path / file_name

    def __str__(self):

        validated_head = (self.validated_data.head()
                         if self.validated_data is not None
                         else 'None')
        print_output = f"\n validated data {validated_head}"

        return print_output

    def _load_data(self) -> pd.DataFrame:

        '''
        Loads the data based on file extension and configured parameters.
        '''

        # Use the stored path attribute
        if not self.full_file_path.exists():
            raise FileNotFoundError(f"File not found at {self.full_file_path}")

        # Determine the file type
        suffix = self.full_file_path.suffix.lower()

        if suffix in ('.xls', '.xlsx'):
            df = pd.read_excel(self.full_file_path, **self.excel_params)
        elif suffix == '.csv':
            # Example for CSV
            df = pd.read_csv(self.full_file_path, **self.excel_params)
        else:
            raise ValueError(f"Unsupported file type: {suffix} at {self.full_file_path}")

        self.raw_data = df

        return df

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Cleans the data by handling missing values and duplicates.
        '''

        # Run throuhgh cleaning steps
        df = df.drop_duplicates()

        return df

    def _validate_inputs(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Validates the data using Pydantic models based model 
        defined in models/XYZ.py.
        Removes invalid records and logs errors.
        '''

        # Access the class constants using self.BOLD and self.END
        bold = self.bold
        end_bold = self.end_bold

        data_list = []
        errors = []

        # Validate each row using Pydantic models
        for _, row in df.iterrows():
            try:
                # The Pydantic model validates the row data during instantiation
                record = Data(**row.to_dict())

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

        id_col = 'insert here'

        idx = pd.to_datetime([r[id_col] for r in data_list])
        df_validated = pd.DataFrame(data_list, index=idx)
        df_validated.index.name = id_col
        df_validated = df_validated.drop(columns=[id_col], errors='ignore')

        # Create DataFrame for error records
        col_names = df.columns.tolist()
        col_names += ['total_errors', 'error_details']

        error_df = pd.DataFrame(errors,
                                columns=col_names)

        # --- Summary Report at the End ---
        total_errors = error_df['total_errors'].sum()

        if total_errors > 0:
            print(f"\n🚨 {total_errors} inputs have failed validation for "
                  f"{bold}insert reference{end_bold} datasets. "
                  "Please investigate further.")

        else:
            print("\n✅ All rows passed validation successfully for "
                  f"{bold}insert reference{end_bold} datasets.")

        self.input_data_errors = error_df
        self.validated_data = df_validated

        return df_validated

    def _transform_data(self, df: pd.DataFrame) -> pd.DataFrame:

        '''
        Completes transformation steps f
        
        Effects:
            a
            b
        
        Note:
            
        '''

        # Run through tranform steps

        self.transformed_data = df

        return df

    def process(self) -> pd.DataFrame:
        '''
        Orchestrates loading, cleaning and validation processes.
        '''

        raw_data = self._load_data()
        cleaned_data = self._clean_data(raw_data)
        validated_data = self._validate_inputs(cleaned_data)
        self._transform_data(validated_data)
        return

    def export_data(self,
                        output_file_name: str,
                        export_errors: bool = False,
                        export_validated: bool = False,
                        output_folder: str = 'reporting') -> None:
        '''
        Exports the selected internal data (errors and/or validated data) 
        to an Excel file, creating a separate sheet for each type.

        Args:
            output_file_name: The name of the output Excel file (e.g., 'data_report.xlsx').
            export_errors: If True, exports self.input_data_errors to 'Input Data Errors' sheet.
            export_validated: If True, exports self.validated_data to 'Validated Data' sheet.
            output_folder: The sub-folder relative to the current working directory.
                            Defaults to 'reporting'.
        '''

        # Prepare data mapping and checks
        data_to_export = []

        input_errors_exist = (
            export_errors and
            hasattr(self, 'input_data_errors') and
            self.input_data_errors is not None and
            not self.input_data_errors.empty
        )

        if input_errors_exist:
            data_to_export.append({
                'df': self.input_data_errors,
                'sheet_name': 'Input Data Errors',
                'description': 'Input Data Errors'
            })

        validated_data_exist = (
            export_validated and
            hasattr(self, 'validated_data') and
            self.validated_data is not None and
            not self.validated_data.empty)

        if validated_data_exist:
            data_to_export.append({
                'df': self.validated_data,
                'sheet_name': 'Validated Data',
                'description': 'Validated Data'
            })

        # Early exit if no data is selected or available
        if not data_to_export:
            if not export_errors and not export_validated:
                print("\n⚠️ No data selected for export. "
                    "Set 'export_errors' or 'export_validated' to True.")
            else:
                # If selected, but the data attribute was None/Empty
                print("\n✅ No available data to export for the selected options.")
            return

        # Convert output_folder string to a Path object relative to CWD
        output_dir = Path.cwd() / output_folder

        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"\n❌ Permission Denied: Cannot create folder at {output_dir}."
                  "Check access rights.")
            return
        except OSError as e:
            print(f"\n❌ General OS Error creating directory '{output_dir}': {e}")
            return

        output_file = output_dir / output_file_name # Final output path

        # Perform the multi-sheet export with robust error handling
        try:
            with pd.ExcelWriter(output_file, datetime_format='dd/mm/yyyy') as writer:
                exported_items = []
                for item in data_to_export:
                    item['df'].to_excel(writer,
                                        sheet_name=item['sheet_name'],
                                        index=False)
                    exported_items.append(item['description'])

            # Success message generation
            bold = self.bold
            end_bold = self.end_bold

            exported_list_str = " and ".join(exported_items)

            print(f"\n✅ Export successful for {bold}insert reference{end_bold}:")
            print(f"   {exported_list_str} exported to **{output_file_name}**.")
            print(f"   Location: {output_file.relative_to(Path.cwd())}")

        except PermissionError:
            print(f"\n❌ Permission Denied: The file {output_file.name} is likely **open**."
                "Please close it and retry.")
            return
        except (OSError, IOError) as e:
            print(f"\n❌ Failed to export data to {output_file}: {e}")
            return
