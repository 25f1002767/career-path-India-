import os
from dotenv import load_dotenv

load_dotenv()

client = None

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key.strip():
        from google import genai
        client = genai.Client(api_key=api_key.strip())
except Exception as e:
    print("Warning: Could not initialize Gemini client:", e)
    client = None