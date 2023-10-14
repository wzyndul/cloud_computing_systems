from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Zastąp wartościami swoimi danymi
connection_string = "DefaultEndpointsProtocol=https;AccountName=dataincloud;AccountKey=0e/NsZI/PrDszy3k/5edZzgRR+v+DHOj6plZ0Z/3rmMuXj+QR1k7c4hWvi+SVKQwRGejytsNmR1p+AStWsN23g==;EndpointSuffix=core.windows.net"
container_name = "test"
blob_name = "dataincloud"
text_to_upload = "Hello, this is a sample text."

# Tworzenie klienta usługi Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Tworzenie kontenera, jeśli nie istnieje
container_client = blob_service_client.get_container_client(container_name)
if not container_client.exists():
    container_client.create_container()

# Tworzenie klienta bloba
blob_client = container_client.get_blob_client(blob_name)

# Wstawianie tekstu jako stringa do bloba
blob_client.upload_blob(text_to_upload, overwrite=True)

print(f"String został wstawiony do bloba {blob_name} w kontenerze {container_name}.")
