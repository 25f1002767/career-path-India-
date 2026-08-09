import os
from pathlib import Path
from dotenv import load_dotenv
from services.ai_client import client
# Load .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

from services.ai_client import client

models_to_test = [
    "models/gemini-3.6-flash",
    "models/gemini-3.5-flash",
    "models/gemini-3.5-flash-lite",
    "models/gemini-3.1-flash-lite",
    "models/gemini-2.5-flash-lite",
    "models/gemini-2.0-flash"
]

for model in models_to_test:
    print(f"\nTesting {model}...")

    try:
        response = client.models.generate_content(
            model=model,
            contents="Reply with only OK."
        )

        print("✅ SUCCESS")
        print(response.text)

    except Exception as e:
        print("❌ FAILED")
        print(e)