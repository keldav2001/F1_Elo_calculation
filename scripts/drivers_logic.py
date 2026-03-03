import azure.functions as func
import os
import json
import requests
from azure.storage.blob import BlobServiceClient
import time

bp = func.Blueprint()

@bp.route(route="f1_drivers", auth_level=func.AuthLevel.ANONYMOUS)
def F1DriversToBlob(req: func.HttpRequest) -> func.HttpResponse:


    connection_string = os.environ.get("AzureWebJobsStorage")
    if not connection_string:
        return func.HttpResponse("Error: AzureWebJobsStorage missing.", status_code=500)
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = "f1data-bronze"

    try:

        container_client = blob_service_client.get_container_client(container_name)

        if not container_client.exists():
            container_client.create_container()

        processed_years = 0

        for year in range(2000, 2026):
            url = f"https://api.jolpi.ca/ergast/f1/{year}/drivers"
            res = requests.get(url, timeout=10)
            time.sleep(1)
            
            if res.status_code == 200:
                drivers = res.json()
                
                blob_name = f"drivers/year={year}/{year}_drivers.json"
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
                blob_client.upload_blob(json.dumps(drivers), overwrite=True)
                processed_years += 1

        return func.HttpResponse(f"Succesful save: {processed_years} years of data saved.", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)