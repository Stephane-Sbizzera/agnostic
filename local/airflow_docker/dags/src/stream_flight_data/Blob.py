import os

from azure.storage.blob import BlobServiceClient

class BlobSamples(object):
    def __init__(self, connection_string, container,blob, dest_file):
        self.connection_string = connection_string
        self.container = container
        self.blob = blob
        self.dest_file = dest_file

    def block_blob_sample(self):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(self.AZURE_CONTAINER_NAME)
        blob_client = container_client.get_blob_client('ls.csv')
        download_file_path = 'test.csv'
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())