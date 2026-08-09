import os
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

env_path = BASE_DIR / ".env"

print("Looking for .env at:")
print(env_path)

loaded = load_dotenv(env_path)

print("Env Loaded:", loaded)

API_KEY = os.getenv("RAPIDAPI_KEY")

print("API KEY =", API_KEY)

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": API_KEY or "",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

params = {
    "query": "Software Engineer in India",
    "page": "1",
    "num_pages": "1"
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

print("Status:", response.status_code)

print(response.text)