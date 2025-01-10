import os
import sys  # Required to modify the Python path dynamically.

# Add the Library folder to the Python path.
script_directory = os.path.dirname(os.path.abspath(__file__))
working_folder = os.path.abspath(os.path.join(script_directory, '..'))
function_library = os.path.abspath(os.path.join(script_directory, 'Library'))
sys.path.append(function_library)  # Add the library folder to the path.

from A_Load_Sales_dataframe import A_Load_Sales_dataframe

  
def main():
    # Define working folder
    input_xlsx = os.path.join(working_folder, 'Pickle_database.xlsx')

    try:
        df_sales = A_Load_Sales_dataframe(input_xlsx)
        print(df_sales.head())  # Proper syntax for calling the DataFrame head method.
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()
