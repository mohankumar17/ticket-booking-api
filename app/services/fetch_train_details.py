import requests
from flask import current_app
from app.utils.custom_exception import DETAILS_NOT_FOUND

def train_details(trainId):
    url = f'http://{current_app.config.get("TRAINS_API_HOST")}:{current_app.config.get("TRAINS_API_PORT")}/api/trains/{trainId}'
    res = requests.get(url=url)

    if res.status_code == 200:
        return res.json()
    else:
        raise DETAILS_NOT_FOUND(f"Train details with ID: {trainId} not found")

