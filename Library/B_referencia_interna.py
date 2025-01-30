import pandas as pd
import numpy as np
import ast  # To safely convert string to dict
import re  # Import regex for better placeholder extraction


"""
Nota en obsidian: Sales Management.md
Archivo requerido: Pickle_database.xlsx un folder antes
"""

def B_generate_dicts(df_input, columns, dictionary_structure, aggregation_column):
    """
    Generate dictionaries dynamically from a DataFrame based on a given structure.
    """

    print("🚀 Step 1: Checking if all placeholders exist in DataFrame columns...\n")

    # 🔹 Step 1: Extract placeholders using regex
    placeholders = re.findall(r"\{(.*?)\}", dictionary_structure)  # Extract text inside {}

    print(f"📌 Found placeholders in structure: {placeholders}\n")
    print(f"📌 Available DataFrame columns: {df_input.columns.tolist()}\n")

    # 🔹 Step 2: Validate that all placeholders exist in df_input.columns
    missing_columns = [col for col in placeholders if col not in df_input.columns]
    
    if missing_columns:
        print(f"❌ ERROR: The following required columns are missing in the DataFrame: {missing_columns}\n")
        print("⚠️ Please check the column names in your DataFrame and dictionary structure.")
        return None  # Stop execution if required columns are missing

    print("✅ All required columns are present in the DataFrame!\n")

    # 🚀 Step 2: Validate that required fields are NOT empty
    print("\n🔍 Step 2: Checking for empty values in required columns...\n")

    empty_columns = [col for col in placeholders if df_input[col].isna().all()]  # Columns that are completely empty

    if empty_columns:
        print(f"⚠️ WARNING: The following columns are completely empty: {empty_columns}\n")
        print("🔹 If this is expected, continue. If not, check your data source.")
    
    print("✅ No completely empty required columns detected!\n")

    # 🚀 Step 3: Validate dictionary structure
    print("\n🛠 Step 3: Validating dictionary structure format...\n")

    # 🔹 Step 3.1: Check for balanced brackets
    open_brackets = dictionary_structure.count("{")
    close_brackets = dictionary_structure.count("}")

    if open_brackets != close_brackets:
        print(f"❌ ERROR: Mismatched brackets detected in dictionary structure.")
        print(f"🔹 Found {open_brackets} opening and {close_brackets} closing brackets.")
        print("⚠️ Please check your structure formatting.")
        return None

    print("✅ Brackets are correctly balanced!\n")

    # 🔹 Step 3.2: Attempt to parse as a dictionary
    try:
        # Replace placeholders with dummy values
        dummy_dict_str = dictionary_structure
        for placeholder in placeholders:
            # Ensure text placeholders get proper quotes
            if placeholder in df_input.select_dtypes(include=[object]).columns:
                dummy_value = f"'TEST_VALUE'"
            else:
                dummy_value = "0"  # Keep numeric fields as numbers

            # Replace placeholder with correct format
            dummy_dict_str = dummy_dict_str.replace(f"{{{placeholder}}}", dummy_value)

        # 🔹 Remove unnecessary spaces, tabs, and line breaks
        cleaned_dict_str = " ".join(dummy_dict_str.split())

        # 🔹 Fix double curly braces (convert `{{` → `{` and `}}` → `}`)
        cleaned_dict_str = cleaned_dict_str.replace("{{", "{").replace("}}", "}")

        # 🔹 Ensure it starts with a curly brace `{`
        if not cleaned_dict_str.startswith("{"):
            cleaned_dict_str = "{" + cleaned_dict_str + "}"

        # 🔹 DEBUG: Print the final dictionary string before parsing
        print(f"🛠️ Debugging - Final Fixed Dictionary String:\n{cleaned_dict_str}\n")

        # 🔹 Additional Debug: Test if it's valid Python syntax before `ast.literal_eval()`
        try:
            compile(cleaned_dict_str, "<string>", "eval")  # This will raise SyntaxError if invalid
        except SyntaxError as e:
            print(f"❌ ERROR: Dictionary structure is still invalid before parsing!\n🔹 Error: {e}")
            return None

        # 🔹 Attempt to parse
        parsed_dict = ast.literal_eval(cleaned_dict_str)
        print(f"✅ Dictionary structure is valid! Sample Output:\n{parsed_dict}\n")

    except Exception as e:
        print(f"❌ ERROR: Dictionary structure is invalid! ⚠️\n")
        print(f"🔹 Error message: {e}\n")
        print("⚠️ Please check your formatting, missing quotes, or misplaced brackets.")
        return None
    print("✅ Dictionary structure validated successfully!\n")

    # 🚀 Step 4: Generate dictionaries for each row
    print("\n🛠 Step 4: Generating dictionary for each row...\n")

    # Initialize an empty list to store dictionary strings
    dict_list = []

    # 🔹 Step 4.1: Iterate over each row in df_input
    for index, row in df_input.iterrows():
        try:
            # Start with the validated dictionary structure
            row_dict_str = dictionary_structure

            # Replace placeholders with actual row values
            for placeholder in placeholders:
                value = row[placeholder]
                # Ensure strings are quoted
                if isinstance(value, str):
                    value = f"'{value}'"
                row_dict_str = row_dict_str.replace(f"{{{placeholder}}}", str(value))

            # 🔹 Remove unnecessary spaces and ensure valid formatting
            row_dict_str = " ".join(row_dict_str.split())  # Normalize whitespace
            row_dict_str = row_dict_str.replace("{{", "{").replace("}}", "}")  # Fix extra brackets
            if not row_dict_str.startswith("{"):
                row_dict_str = "{" + row_dict_str + "}"  # Ensure it's enclosed in {}

            # 🔹 Append the generated dictionary as a string to the list
            dict_list.append(row_dict_str)

        except Exception as e:
            print(f"⚠️ ERROR processing row {index}: {e}")

    # 🔹 Step 4.2: Store results in a new DataFrame column
    df_output = df_input.copy()
    df_output["Dict"] = dict_list

    print("✅ Dictionary generation completed!\n")

    # 🔹 Debugging: Show sample output
    print("\n📌 Sample Generated Dictionaries:")
    print(df_output[["Orden", "Dict"]].head())

    return df_output  # Temporarily return None to focus on debugging Step 1 only




def B_generate_orden_dicts(df_sales):
    """
    Generate strings formatted as dictionaries in a DataFrame based on input data.
    
    Args:
        df_sales (pd.DataFrame): Input DataFrame with columns ['Orden', 'Clave', 'Piezas', 'Precio', 'Contrato', 
                                                              'Fecha_maxentrega', 'EstatusCliente'].
    
    Returns:
        pd.DataFrame: DataFrame containing processed dictionary-like strings.
    """
    def generate_value_total_info(row):
        #print("\n\tFunción para convertir en diccionarios corriendo\n")
        """Helper function to generate 'Comercial' value."""
        sku_column = row['Clave']
        key_dict = row['Orden']
        if pd.isna(sku_column) or sku_column == '':
            return f"{key_dict}: Skipped"
        elif isinstance(sku_column, str) and sku_column.startswith('{'):
            return f"{{'{key_dict}': {sku_column}}}"
        elif isinstance(sku_column, str) and sku_column.startswith('0'):
            return f"{{'{key_dict}': {{'{sku_column}': ({row['Piezas']}, {row['Precio']})}}}}"
        else:
            return f"{key_dict}: Skipped"

    def generate_value_contrato(row):
        """Helper function to generate 'Contratos' value."""
        return f"{{'{row['Orden']}': {row['Contrato']}}}"

    def generate_value_logistica(row):
        """Helper function to generate 'Logistica' value."""
        return f"{{'{row['Orden']}': {{'Fecha_max': '{row['Fecha_maxentrega']}', 'Estatus_cliente': '{row['EstatusCliente']}'}}}}"

    # Generate the new column
    df_sales['Comercial'] = df_sales.apply(generate_value_total_info, axis=1)
    df_sales['Contratos'] = df_sales.apply(generate_value_contrato, axis=1)
    df_sales['Logistica'] = df_sales.apply(generate_value_logistica, axis=1)

    # Select relevant columns for the final dictionary DataFrame
    df_dicts = df_sales[['Orden', 'Comercial', 'Contratos', 'Logistica']].copy()
    
    return df_dicts

