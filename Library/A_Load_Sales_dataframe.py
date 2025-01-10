# .\Library\A_Load_Sales_dataframe.py

import os
import pandas as pd  # Include the pandas import for the function to work.

def A_Load_Sales_dataframe(excel_file):
    """
    Load sales data from an Excel file if it exists.
    
    Args:
        excel_file (str): Path to the Excel file.
    
    Returns:
        pd.DataFrame: DataFrame containing the sales data.
    """
    if os.path.exists(excel_file):  # Check if the file exists.
        df_sales = pd.read_excel(excel_file)  # Load the Excel file into a DataFrame.
    else:
        raise FileNotFoundError(f"The file '{excel_file}' does not exist.")
    
    return df_sales
