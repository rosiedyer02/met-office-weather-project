import os
import requests
from dotenv import load_dotenv
from parser import parse_forecast
from storage import save_forecasts

load_dotenv()

API_KEY = os.getenv("DATAHUB_API_KEY")
BASE_URL = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/daily"

# Plymouth coordinates
params = {
    "latitude": 50.3755,
    "longitude": -4.1427
}

headers = {
    "apikey": API_KEY,
    "accept": "application/json",
}

response = requests.get(BASE_URL, headers=headers, params=params)

if response.status_code == 200:
    forecasts = parse_forecast(response.json())
    save_forecasts("Plymouth", forecasts)
    print(f"Saved {len(forecasts)} days of forecast data for Plymouth")
else:
    print(f"Request failed: {response.status_code}")