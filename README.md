
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


--------------------------------------------------------------------

1. Para los ids nulos ¿Qué sugieres hacer con ellos ?
   - En este caso se eliminan y no forman parte de la agregacion y asi no afectar el reporte derivado antes de saber que es lo que esta pasando, luego se imprime una alerta para que este problema sea investigado ya que en una base de transacciones nunca deberia haber ingresos o egresos con identificadores faltantes
2. Considerando las columnas name y company_id ¿Qué inconsistencias notas y como las mitigas?
   - En ambas columnas se observan datos faltantes y erroneos, ya que los errores son minoria, la solucion es crear un mapa donde la combinacion por cada company_id y name mas comun sea la que prevalesca, por ejemplo si el company_id 1 tiene 20 filas con name X, y solo 5 con name Y, el name Y sera reemplazado por el name X en todas las filas
3. Para el resto de los campos ¿Encuentras valores atípicos y de ser así cómo procedes?
  - No se encontraron transacciones pagadas sin fecha de pago
  - Se encontraron IDs de transaccion faltantes
  - Se encontraron transacciones con fechas de pago validas, pero con status de pago erroneo, entonces a todas las filas con fecha de pago valida, se les asigna el status paid
4. ¿Qué mejoras propondrías a tu proceso ETL para siguientes versiones?
  - Realizar optimizaciones para grandes cantidades de datos, como utilizar un mapeo vectorizado en lugar de apply, reducir la cantidad de groupbys, y filtrar los datos lo antes posible

