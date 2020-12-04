import os
import airflow
from airflow import DAG
from airflow.contrib.sensors.wasb_sensor import WasbBlobSensor
from airflow.contrib.hooks.wasb_hook import WasbHook
from airflow.operators import PythonOperator
from src.stream_flight_data.Blob import BlobSamples

connection_string = 'xxxx'
AZURE_CONTAINER_NAME = 'tfstate'
account_name = 'terraformaccount2'

BLOB_NAME = 'ls.csv'

bl = BlobSamples(connection_string, AZURE_CONTAINER_NAME, BLOB_NAME,'test.csv')

def callAzure():
    bl.block_blob_sample()

args = {
    'owner': 'airflow',
    'description': 'spark Consumer via bash Operator in same container',
    'start_date': airflow.utils.dates.days_ago(1),       # this in combination with catchup=False ensures the DAG being triggered from the current date onwards along the set interval
    'provide_context': True,
}

dag = DAG(
    dag_id='azure_DAG',
    default_args=args,
    schedule_interval='@daily',  # set interval
    catchup=False,
)


wait_for_blob = WasbBlobSensor(
    task_id="wait_for_blob",
    wasb_conn_id=connection_string,
    container_name=AZURE_CONTAINER_NAME,
    blob_name=BLOB_NAME,
    dag=dag
)

task1 = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=callAzure,
dag=dag)

wait_for_blob >> task1

