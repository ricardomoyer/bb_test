
Este repositorio contiene un proceso de datos construido con Apache Airflow para limpiar, procesar y agregar datos de ventas desde un archivo CSV alojado en GitHub. El pipeline descarga los datos en bruto, los limpia y formatea, agrega las ventas por cliente y mes, y sube los datos procesados de nuevo a GitHub.

## Características
- Limpia los datos de ventas sin procesar eliminando las filas no válidas y filtrando en función de criterios predefinidos.
- Formatea y analiza las columnas de fecha para garantizar la coherencia.
- Agrega los datos de ventas por nombre de cliente y mes-año para su análisis.
- Sube automáticamente los datos procesados a una carpeta especificada en el repositorio de GitHub.

## Requisitos
- Apache Airflow](https://airflow.apache.org/) instalado y en ejecución.
- Python 3.7 o posterior.

## Configuración y uso

### Paso 1: Clonar el repositorio

git clone https://github.com/ricardomoyer/bb_test.git
cd bb_test
### Paso 2: Configurar Airflow
Asegúrese de que su entorno Airflow está configurado correctamente. Coloque el DAG (ejercicio1_pipeline.py) en la carpeta dags de su instalación de Airflow.

### Paso 3: Instalar dependencias
Instale los paquetes Python necesarios en su entorno Airflow:


pip install pandas peticiones
### Paso 4: Añadir Token de GitHub 
Para subir el archivo procesado de nuevo a GitHub, asegúrese de que su token de la API de GitHub está incluido en el código. Reemplace el TOKEN en la función process_and_save:

headers = {«Authorization»: f «token YOUR_GITHUB_TOKEN»}

### Paso 5: Ejecutar el pipeline


En la interfaz de usuario de Airflow, active el DAG github_data_processing.

### Paso 6: Resultados
Los datos limpiados y procesados se cargarán en la carpeta ejercicio1/processed de este repositorio.
