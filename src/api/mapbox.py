import requests
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
is_loaded = load_dotenv()
print(f"Was .env loaded successfully? {is_loaded}") 

def forward_geocode_mapbox(query: str):
    access_token = os.getenv("MAPBOX_ACCESS_TOKEN")

    url = (
        f"https://api.mapbox.com/search/geocode/v6/forward"
        f"?q={query}"
        f"&country=us"
        f"&access_token={access_token}"
    )

    response = requests.get(url)
    response.raise_for_status()

    return response.json()

def reverse_geocode_mapbox(latitude: float, longitude: float):
    access_token = os.getenv("MAPBOX_ACCESS_TOKEN")

    url = (
        f"https://api.mapbox.com/search/geocode/v6/reverse"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&country=us"
        f"&access_token={access_token}"
    )

    response = requests.get(url)
    response.raise_for_status()

    return response.json()