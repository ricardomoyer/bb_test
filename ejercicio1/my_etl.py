from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import requests
import os


from data_processing import process_data

#define argumentos default
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

#definir el dag
with DAG(
    'github_data_processing',
    default_args=default_args,
    description='Clean and process data from GitHub',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    def download_file():

        """Descarga un archivo CSV desde un repositorio de GitHub.

        El archivo descargado se guarda localmente en `/tmp/data_prueba_tecnica.csv`.

        Arroja:
            HTTPError: Si falla la descarga."""
        
        url = "https://raw.githubusercontent.com/ricardomoyer/bb_test/main/ejercicio1/raw/data_prueba_tecnica.csv"
        response = requests.get(url)
        with open('/tmp/data_prueba_tecnica.csv', 'wb') as f:
            f.write(response.content)

    def process_and_save():

        """
        Procesa el archivo CSV descargado y sube el archivo procesado a GitHub.

        La función realiza los siguientes pasos:
        1. Lee el archivo CSV sin procesar de `/tmp/data_prueba_tecnica.csv`.
        2. Procesa los datos utilizando la función `process_data`.
        3. Guarda los datos procesados en `/tmp/datos_procesados.csv`.
        4. Sube el archivo procesado al repositorio en GitHub.

        Arroja:
            HTTPError: Si la subida a GitHub falla.
        
        """
        input_file = '/tmp/data_prueba_tecnica.csv'
        output_file = '/tmp/processed_data.csv'

        #procesar los datos
        processed_data = process_data(input_file)
        processed_data.to_csv(output_file, index=False)

        #sube el archivo a github
        with open(output_file, 'rb') as f:
            content = f.read().decode('utf-8')
        url = "https://api.github.com/repos/ricardomoyer/bb_test/contents/ejercicio1/processed/processed_data.csv"
        headers = {"Authorization": f"token "}

        import base64

        #codifica el contenido en utf-8
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

        data = {
            "message": "Add processed data",
            "content": encoded_content,
            "branch": "main"
        }
        requests.put(url, headers=headers, json=data)
        

    download_task = PythonOperator(
        task_id='download_file',
        python_callable=download_file,
    )

    process_task = PythonOperator(
        task_id='process_and_save',
        python_callable=process_and_save,
    )

    download_task >> process_task
