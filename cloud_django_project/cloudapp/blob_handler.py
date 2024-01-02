from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from azure.storage.blob import BlobServiceClient


def create_blob_container(user):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)

    container_client = blob_service_client.get_container_client(user.username.lower())
    if not container_client.exists():
        container_client.create_container()


def upload_blob(user, file):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(user.username.lower())

    blob_client = container_client.get_blob_client(file.name)
    blob_client.upload_blob(file, overwrite=True)


def parallel_upload_blob(user, files):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(upload_blob, user, file) for file in files]

    for future in futures:
        future.result()


def list_blobs(user):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(user.username.lower())

    blob_list = container_client.list_blobs()
    return blob_list
