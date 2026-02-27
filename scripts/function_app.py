import azure.functions as func
import os
import json
import pandas as pd
import requests
from azure.storage.blob import BlobServiceClient
import io

app = func.FunctionApp()

@app.route(route="f1_to_storage", auth_level=func.AuthLevel.ANONYMOUS)
def F1DataToBlob(req: func.HttpRequest) -> func.HttpResponse:
    
    all_years_data = []
    seen_drivers = {}

    try:

        for year in range(1950, 2026):
            url = f"https://api.jolpi.ca/ergast/f1/{year}/drivers"
            res = requests.get(url, timeout=10)
            
            if res.status_code == 200:
                drivers = res.json()["MRData"]["DriverTable"]["Drivers"]
                
                for d in drivers:
                    d_id = d['driverId']

                    if d_id not in seen_drivers:
                        seen_drivers[d_id] = year
                        d['debut_year'] = year 
                        all_years_data.append(d)
        
        
        df = pd.DataFrame(all_years_data)
        
        connection_string = os.environ.get("AzureWebJobsStorage")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = "f1data-bronze"
        
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()

        blob_client = blob_service_client.get_blob_client(container=container_name, blob="master_drivers.json")
        blob_client.upload_blob(df.to_json(orient='records'), overwrite=True)

        return func.HttpResponse(f"{len(df)} db pilóta mentve a Blob-ba.", status_code=200)

    except Exception as e:
        return func.HttpResponse(f" Hiba: {str(e)}", status_code=500)