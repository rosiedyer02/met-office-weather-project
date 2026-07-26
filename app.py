import os
import requests
from parser import parse_forecast
from storage import save_forecasts

BASE_URL = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/daily"

LOCATIONS = {
    "Plymouth": {"latitude": 50.3755, "longitude": -4.1427},
}

def lambda_handler(event, context):
    api_key = os.getenv("DATAHUB_API_KEY")
    headers = {"apikey": api_key, "accept": "application/json"}

    results = {}
    for location, coords in LOCATIONS.items():
        response = requests.get(BASE_URL, headers=headers, params=coords)

        if response.status_code == 200:
            forecasts = parse_forecast(response.json())
            save_forecasts(location, forecasts)
            results[location] = f"saved {len(forecasts)} days"
            print(f"Successfully saved {len(forecasts)} days for {location}")
        else:
            print(f"Request failed for {location}: status={response.status_code}, body={response.text}")
            results[location] = f"failed: {response.status_code}"

    return {"statusCode": 200, "body": results}