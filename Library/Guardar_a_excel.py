import os
import pandas as pd

def save_df_to_excel(input_df, filename, output_directory):
    """
    Save a DataFrame to an Excel file in the specified directory.

    Args:
        input_df (pd.DataFrame): DataFrame to save.
        filename (str): Name of the output file (without extension).
        output_directory (str): Directory where the file will be saved.
    
    Returns:
        None
    """
    file_path = os.path.join(output_directory, f"{filename}.xlsx")
    
    while True:
        try:
            # Attempt to save the file
            input_df.to_excel(file_path, index=False, engine='openpyxl')
            print(f"\nFile '{filename}.xlsx' saved to {output_directory}")
            break
        except PermissionError:
            # Handle the case where the file is in use
            input(f"\nThe file '{filename}.xlsx' is in use. Please close the file and press Enter to retry.\n")
