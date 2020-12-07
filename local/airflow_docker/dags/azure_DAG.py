import os
from json import dump, dumps
# Airflow
import airflow
from airflow import DAG
from airflow.providers.microsoft.azure.sensors.wasb import WasbBlobSensor
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.operators import PythonOperator
#HDFS
from hdfs import InsecureClient
# Utils
# from src.stream_flight_data.Blob import BlobSamples

from airflow.providers.microsoft.azure.sensors.wasb import WasbBlobSensor
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow import settings
from airflow.models import Connection

account_name = 'terraformaccount2'
key = 'xxxxxxx'
conn_id='wasb_default'

conn = Connection(
        conn_id=conn_id,
        login=account_name,
        password=key,
) #create a connection object
session = settings.Session() # get the session
session.add(conn)
session.commit() # it will insert the connection object programmatically.
hook = WasbHook(wasb_conn_id='wasb_default')
AZURE_CONTAINER_NAME = 'tfstate'
blob_name ='ls.csv'
file_path = '../'


# Azure strings
connection_string = 'DefaultEndpointsProtocol=https;AccountName=terraformaccount2;AccountKey=R+7/s6BFH+O+qCmdOfRrBdls94+VqkA51KwT/xOig5Hsl+LiHZJ7hv8zN36InVhWfNf46g5YVlNcpB6JtqUZRQ==;EndpointSuffix=core.windows.net'
AZURE_CONTAINER_NAME = 'tfstate'
account_name = 'terraformaccount2'
BLOB_NAME = 'ls.csv'

# bl = BlobSamples(connection_string, AZURE_CONTAINER_NAME, BLOB_NAME,'test.csv')

def callAzure():
    print('Hello')
    hook.get_file(file_path, AZURE_CONTAINER_NAME, blob_name)

def write_to_hdfs():
    records = [
        {'name': 'foo', 'weight': 1},
        {'name': 'bar', 'weight': 2},
    ]

    # As a context manager:
    client = InsecureClient('http://namenode:9000', user='ann')
    with client.write('data/records.jsonl', encoding='utf-8') as writer:
        dump(records, writer)

    # Or, passing in a generator directly:
    client.write('data/records.jsonl', data=dumps(records), encoding='utf-8')

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


# wait_for_blob = WasbBlobSensor(
#     task_id="wait_for_blob",
#     wasb_conn_id=connection_string,
#     container_name=AZURE_CONTAINER_NAME,
#     blob_name=BLOB_NAME,
#     dag=dag
# )

wait_for_blob = WasbHook(
    task_id="wait_for_blob",
    wasb_conn_id=connection_string,
    container_name=AZURE_CONTAINER_NAME,
    blob_name=BLOB_NAME,
    dag=dag
)

task1 = PythonOperator(
    task_id='download_from_azure',
    provide_context=True,
    python_callable=callAzure,
dag=dag)

task2 = PythonOperator(
    task_id='push_to_hdfs',
    provide_context=True,
    python_callable=write_to_hdfs,
dag=dag)

wait_for_blob >> task1

