import requests
import os

API_KEY = os.getenv("RAILWAY_API_KEY")
BASE_URL = "https://api.railwayapi.com/v2"  # example

def fetch_live_status(train_no: str):
    resp = requests.get(
        f"{BASE_URL}/live/train/{train_no}",
        params={"apikey": API_KEY},
        timeout=10
    )
    resp.raise_for_status()
    return resp.json()