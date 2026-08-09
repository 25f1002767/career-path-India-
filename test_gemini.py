import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

print("API Key:", os.getenv("GEMINI_API_KEY"))

from services.ai_client import client

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say Hello"
)

print(response.text)