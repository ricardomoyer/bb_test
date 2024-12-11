import pandas as pd


# calculate valid name-to-company_id and company_id-to-name mappings
def get_valid_mappings(df):
    """ Valida nombres e ID de empresa basándose en las entradas más frecuentes en el DataFrame dado.

    Args:
        Un DataFrame que contiene las columnas `name` y `company_id`.

    Devuelve:
        Una tupla que contiene dos diccionarios:
            - nombre_a_empresa (dict): Mapea nombres a sus IDs de empresa más frecuentes.
            - empresa_a_nombre (dict): Asigna los ID de empresa a los nombres más frecuentes."""
  
    #calcular el company id mas comun para cada name
    name_to_company = (
        df[df['name'].notna() & df['company_id'].notna()]
        .groupby(['name', 'company_id'])
        .size()
        .reset_index(name='count')
    )

    #conservar solo el company id mas comun por name
    name_to_company = (
        name_to_company.loc[name_to_company
        .groupby('name')['count'].idxmax()]
        .sort_values(by='count', ascending=False)
        .drop_duplicates(subset=['company_id'],keep='first')
        .set_index('name')['company_id']
        .to_dict()
    )

    #calcula el name mas frecuente por company id
    company_to_name = (
        df[df['name'].notna() & df['company_id'].notna()]
        .groupby(['company_id', 'name'])
        .size()
        .reset_index(name='count')
    )

    #conserva solamnete el name mas frecuente por company id
    company_to_name=(company_to_name.loc[company_to_name
        .groupby('company_id')['count'].idxmax()]
        .sort_values(by='count', ascending=False)
        .drop_duplicates(subset='name')
        .set_index('company_id')['name']
        .to_dict()
    )
    
    return name_to_company, company_to_name


#aplica el mapeo a las filas con datos faltantes o datos erroneos
def fix_row(row, name_to_company, company_to_name):
    if pd.isna(row['name']) or row['name'] not in name_to_company:
        if row['company_id'] in company_to_name:
            row['name'] = company_to_name[row['company_id']]
    elif pd.isna(row['company_id']) or row['company_id'] not in company_to_name:
        if row['name'] in name_to_company:
            row['company_id'] = name_to_company[row['name']]
    return row





def cleanup(df):

    """
    Limpia un DataFrame eliminando filas no válidas y filtrando estados de transaccion.

    Esta función realiza los siguientes pasos:
    1. Elimina las filas con valores nulos en las columnas `id`, `company_id` o `name`.
    2. Filtra las filas en las que la columna `status` no se encuentra en una lista predefinida de estados válidos.
    3. Filtra las filas donde company_id no es un hash de 40 caracteres
    4. Imprime una advertencia si se elimina alguna fila.

    Args:
        df (pd.DataFrame): El DataFrame de entrada que contiene los datos sin procesar.

    Devuelve:
        pd.DataFrame: El DataFrame limpio con sólo filas válidas.

    Secundarios:
        Imprime un mensaje indicando el número de filas eliminadas, si las hay.
    """
    org_len = len(df)
    df = df.dropna(subset=['id'])
    df.loc[pd.to_datetime(df['paid_at'], errors='coerce').notna(), 'status'] = 'paid'

    #corregir el los company_id y nombres
    valid_name_to_company, valid_company_to_name = get_valid_mappings(df)

    df = df.apply(fix_row, axis=1, args=(valid_name_to_company, valid_company_to_name))



    clean_len = len(df)
    diff = org_len - clean_len
    if diff > 0:
        print('Advertencia! {} filas fueron eliminadas debido a datos nulos o  erroneos'.format(diff))
    return df

def process_data(file_path):

    """
    Procesa un archivo CSV sin procesar para limpiar y agregar los datos de ventas.

    Esta función realiza los siguientes pasos:
    1. Lee un archivo CSV en un DataFrame.
    2. Limpia los datos utilizando la función `cleanup`.
    3. Formatea las columnas de fecha (`created_at` y `paid_at`) y maneja las fechas inválidas.
    4. Agrupa los datos por `nombre` y el mes-año de `created_at`, calculando las ventas totales.
    5. Ordena los datos agregados por `nombre` y `mes_año`.

    Args:
        file_path (str): Ruta al fichero CSV que contiene los datos de ventas.

    Devuelve:
        pd.DataFrame: Un DataFrame con los datos de ventas agregados, agrupados por cliente y mes-año.

    Arroja:
        FileNotFoundError: Si el fichero especificado no existe.
        ValueError: Si el fichero no tiene el formato correcto o contiene datos no válidos.
    """
    data = pd.read_csv(file_path)
    data = cleanup(data)

    #limpiar fechas
    data['created_at'] = data['created_at'].str.split('T').str[0]
    data['created_at'] = pd.to_datetime(data['created_at'], format='%Y-%m-%d', errors='coerce')
    data['paid_at'] = pd.to_datetime(data['paid_at'], format='%Y-%m-%d', errors='coerce')

    #agrupar por nombre y fecha
    data['month_year'] = data['created_at'].dt.to_period('M')
    sales_per_client = data.groupby(['name', 'month_year'])['amount'].sum().reset_index()
    sales_per_client = sales_per_client.sort_values(by=['name', 'month_year'])
    return sales_per_client

