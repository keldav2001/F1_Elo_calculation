import azure.functions as func
import os
import requests
from azure.storage.blob import BlobServiceClient
from drivers_logic import bp as drivers_bp
from results_logic import bp as results_bp

app = func.FunctionApp()

app.register_blueprint(drivers_bp)
app.register_blueprint(results_bp)