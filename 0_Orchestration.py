# Librerías externas
import os
import sys  # Required to modify the Python path dynamically.
import pprint
script_directory = os.path.dirname(os.path.abspath(__file__))
working_folder = os.path.abspath(os.path.join(script_directory, '..'))
function_library = os.path.abspath(os.path.join(script_directory, 'Library'))
sys.path.append(function_library)  # Add the library folder to the path.
# Librerías internas
from A_Load_Sales_dataframe import A_Load_Sales_dataframe
from B_referencia_interna import B_generate_orden_dicts, B_generate_dicts
from Guardar_a_excel import save_df_to_excel
 
def main():
    # Define working folder
    input_xlsx = os.path.join(working_folder, 'Pickle_database.xlsx')
    print("Pickle database loaded")
    try:
        df_sales = A_Load_Sales_dataframe(input_xlsx)
    except FileNotFoundError as e:
        print(e)

    dic_structure = """ 
                    {Orden}: {{
                        {Clave}: {{
                            'Cantidad': {Piezas},
                            'Precio': {Precio} 
                        }} 
                    }}
                    """

    # Generate dictionary
    sales_dict = B_generate_dicts(df_sales, ['Orden', 'Clave', 'Piezas', 'Precio'], dic_structure, 'Orden')
    pprint.pprint(sales_dict)
    filename = 'Dict_repository'
    save_df_to_excel(sales_dict, filename, working_folder)
if __name__ == "__main__":
    main()
