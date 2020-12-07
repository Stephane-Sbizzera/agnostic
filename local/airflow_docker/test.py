from airflow.providers.microsoft.azure.sensors.wasb import WasbBlobSensor
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow import settings
from airflow.models import Connection

account_name = 'terraformaccount2'
key = 'xxxxxx'
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
connection_string = 'DefaultEndpointsProtocol=https;AccountName=terraformaccount2;AccountKey='xxx';EndpointSuffix=core.windows.net'
# hook.get_file(file_path, AZURE_CONTAINER_NAME, blob_name)