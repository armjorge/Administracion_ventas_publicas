import os
import sys  # Required to modify the Python path dynamically.

# Add the Library folder to the Python path.
script_directory = os.path.dirname(os.path.abspath(__file__))
working_folder = os.path.abspath(os.path.join(script_directory, '..'))
function_library = os.path.abspath(os.path.join(script_directory, 'Library'))
sys.path.append(function_library)  # Add the library folder to the path.

from A_Load_Sales_dataframe import A_Load_Sales_dataframe
from B_referencia_interna import B_generate_orden_dicts
from Guardar_a_excel import save_df_to_excel


  
def main():
    # Define working folder
    input_xlsx = os.path.join(working_folder, 'Pickle_database.xlsx')

    try:
        df_sales = A_Load_Sales_dataframe(input_xlsx)
        print(df_sales.head())  # Proper syntax for calling the DataFrame head method.
        # Generate the internal reference dictionary
        df_referencia_interna = B_generate_orden_dicts(df_sales)
        if not df_referencia_interna.empty:
            print("\nDiccionario de Referencia Interna generado:")
            print(df_referencia_interna.head())
            filename = 'Dict_repository'
            save_df_to_excel(df_referencia_interna, filename, working_folder)
        else:
            print("\nDiccionario de Referencia Interna is empty.")

    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()
