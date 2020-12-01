import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.stream_flight_data.WASB import WasbHook

azure = WasbHook(wasb_conn_id='connect_to_azure')

args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(2)}

dag = DAG(
    dag_id="wasb_sensor_test",
    default_args=args,
    schedule_interval=None,
    tags=['poc', 'azure'])


def get_blob_list():
    blob_list = azure.check_for_prefix(container_name='MY_CONTAINER_NAME', prefix='MY_PREFIX')


print_blob_list = PythonOperator(
    task_id='get_blob_list',
    python_callable=get_blob_list,
    dag=dag)

print_blob_list