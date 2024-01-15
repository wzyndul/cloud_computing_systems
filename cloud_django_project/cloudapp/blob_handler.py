from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from azure.storage.blob import BlobServiceClient
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path


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


def list_blobs_with_properties(user):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(user.username.lower())
    blob_list = container_client.list_blobs(include=['versions'])

    files_with_properties = {}
    for blob in blob_list:
        file_name = blob.name
        version_id = blob.version_id
        last_modified = blob.last_modified
        size = blob.size

        if file_name not in files_with_properties:
            files_with_properties[file_name] = []

        files_with_properties[file_name].append({
            'version_id': version_id,
            'last_modified': last_modified,
            'size': size
        })
    return files_with_properties


def change_blob_version(user, file_name, version):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(user.username.lower())

    blob_client = container_client.get_blob_client(file_name)
    blob_client.start_copy_from_url(
        f'https://dataincloud.blob.core.windows.net/{user.username.lower()}/{file_name}?versionId={version}')
    blob_client.delete_blob(version_id=version)


def download_blob(user, file_name):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(user.username.lower())

    blob_client = container_client.get_blob_client(file_name)
    blob_data = blob_client.download_blob().readall()
    response = HttpResponse(blob_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{escape_uri_path(file_name)}"'

    return response
