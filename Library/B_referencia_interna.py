import pandas as pd
import numpy as np

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

    # Generate the new columns
    df_sales['Comercial'] = df_sales.apply(generate_value_total_info, axis=1)
    df_sales['Contratos'] = df_sales.apply(generate_value_contrato, axis=1)
    df_sales['Logistica'] = df_sales.apply(generate_value_logistica, axis=1)

    # Select relevant columns for the final dictionary DataFrame
    df_dicts = df_sales[['Orden', 'Comercial', 'Contratos', 'Logistica']].copy()
    
    return df_dicts
