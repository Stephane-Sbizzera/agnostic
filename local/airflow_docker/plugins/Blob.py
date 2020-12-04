import os

class BlobSamples(object):
    def __init__(self, connection_string, container,blob, dest_file):
        self.connection_string = connection_string
        self.container = container
        self.blob = blob
        self.dest_file = dest_file

    def block_blob_sample(self):

        # Instantiate a new BlobServiceClient using a connection string
        from azure.storage.blob import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        # Instantiate a new ContainerClient
        container_client = blob_service_client.get_container_client(self.container)

        try:
            # Create new Container in the service
            # container_client.create_container()

            # Instantiate a new BlobClient
            blob_client = container_client.get_blob_client("myblockblob")

            # [START download_a_blob]
            with open(self.DEST_FILE, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())
            # [END download_a_blob]

            # [START delete_blob]
            # blob_client.delete_blob()
            # [END delete_blob]

        finally:
            # Delete the container
            container_client.delete_container()