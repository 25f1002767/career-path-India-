import os
from google import genai

client = None

try:
    api_key = os.getenv("GEMINI_API_KEY")

    from services.ai_client import client

except Exception:
    client = None