import os
from json import dump, dumps
# Airflow
import airflow
import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
#HDFS
# from hdfs import InsecureClient
import pyspark
from pyspark.sql import SparkSession
# Utils
from airflow import settings
from airflow.models import Connection
from airflow.providers.microsoft.azure.sensors.wasb import WasbBlobSensor, WasbPrefixSensor
from airflow.sensors.hdfs_sensor import HdfsSensor
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import subprocess
from airflow import DAG
from airflow.sensors.hdfs_sensor import HdfsSensor
from airflow.operators.bash_operator import BashOperator
import datetime
from airflow.operators.python_operator import PythonOperator
import subprocess
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.sensors import ExternalTaskSensor
# Set hook
hook = WasbHook(wasb_conn_id='wasb_default')

AZURE_CONTAINER_NAME = 'tfstate'
blob_name ='ls.csv'
file_path = './data/ls.csv'

# hook.get_file(file_path, AZURE_CONTAINER_NAME, blob_name)

def callAzure(**kwargs):
    file_path = kwargs['file_path']
    AZURE_CONTAINER_NAME = kwargs['AZURE_CONTAINER_NAME']
    blob_name = kwargs['blob_name']
    hook = kwargs['hook']
    try:
        hook.get_file(file_path, AZURE_CONTAINER_NAME, blob_name)
    except Exception as e:
        print (e)
    # hook.check_for_blob(AZURE_CONTAINER_NAME, blob_name)
    return 'Download Done'

def write_to_spark(**kwargs):    
    spark = SparkSession.builder.master("local[*]").appName("azure_access").getOrCreate()
    sc =  spark.sparkContext
    URI = sc._gateway.jvm.java.net.URI
    Path = sc._gateway.jvm.org.apache.hadoop.fs.Path
    FileSystem = sc._gateway.jvm.org.apache.hadoop.fs.FileSystem
    Configuration = sc._gateway.jvm.org.apache.hadoop.conf.Configuration
    IOUtils = sc._gateway.jvm.org.apache.commons.io.IOUtils    
    hdfs = FileSystem.get(URI("hdfs://namenode:9000"), Configuration())
    fileName = kwargs['file_path']
    blob_name = kwargs['blob_name']
    targetPath = "hdfs://namenode:9000/input/{}".format(blob_name)
    hdfs.copyFromLocalFile(True, True, Path(fileName), Path(targetPath))

def pipeline(**kwargs):
    command2 = '/usr/spark/bin/spark-submit --master local[*] --py-files /home/lib/profiling.zip --driver-class-path /home/jars/postgresql-42.2.18.jar --jars /home/jars/dlh-dq-core-0.1.jar,/home/jars/postgresql-42.2.18.jar /home/work/batch/main_profiling.py'
    proc2 = subprocess.run(command2.split(' '))
    return "KWARGS: {}".format("Pipeline done")

args = {'owner': 'airflow',
                'depends_on_past': False,
                'provide_context': True,
                'start_date': datetime.datetime(2020, 12, 5, 0, 0),
                'email_on_failure': True,
                'email_on_retry': False,
                'retries': 0,
                'concurrency': 1
                }

dag = DAG(
    dag_id='azure_DAG',
    default_args=args,
    schedule_interval=None,  # set interval
    catchup=False,
)

wait_for_blob = WasbPrefixSensor(
    task_id="wait_for_blob",
    wasb_conn_id='wasb_default',
    timeout=18*60*60,
    poke_interval=5,
    container_name=AZURE_CONTAINER_NAME,
    blob_name=blob_name,
    prefix ='*',
    dag=dag
)

task1 = PythonOperator(
    task_id='download_from_azure',
    provide_context=True,
    python_callable=callAzure,
    trigger_rule='all_success',
    op_kwargs={'AZURE_CONTAINER_NAME': AZURE_CONTAINER_NAME, 'blob_name': blob_name,'file_path':file_path, 'hook': hook},
    dag=dag)


source_data_sensor = HdfsSensor(
    task_id='hdfs_source_data_sensor',
    filepath='/input/*ls.csv',
    hdfs_conn_id='webhdfs_default',
    poke_interval=6,
    trigger_rule='one_success',
    timeout=60,
    dag=dag
)

task3 = PythonOperator(
    task_id='push_to_hdfs',
    provide_context=True,
    python_callable=write_to_spark,
    trigger_rule='all_success',
    op_kwargs={'file_path': file_path, 'blob_name': blob_name},
    dag=dag)

source_data_sensor.set_upstream(wait_for_blob)
task3.set_upstream(task1)
task1.set_upstream(wait_for_blob)
t4 = PythonOperator(task_id="DEEQU_Profiling", provide_context=True, python_callable=pipeline, dag=dag,     trigger_rule='all_success')

t4.set_upstream(source_data_sensor)

wait_for_blob >> task1 >> task3 
source_data_sensor >> t4
    