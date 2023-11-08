from django.conf import settings
from azure.storage.blob import BlobServiceClient


def create_blob_container(user):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)

    container_client = blob_service_client.get_container_client(user.username.lower())
    if not container_client.exists():
        container_client.create_container()


def upload_blob(user): # container_name = nazwa uzytkownika, trzeba to jakos lepiej ogarnac
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(user.username.lower())

    blob_name = "pliczek_tekstowy.txt"
    text_to_upload = "Hello, this is a sample text."

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(text_to_upload, overwrite=True)

