import os
import requests
from dotenv import load_dotenv

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

print("Status code:", response.status_code)
print(response.json())