import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# ==========================================================
# Load Environment Variables
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("CareerPath India AI")
print("Project Root :", BASE_DIR)
print("API Key Loaded :", "YES" if API_KEY else "NO")
print("=" * 60)

# ==========================================================
# Gemini Client
# ==========================================================

from services.ai_client import client

# ==========================================================
# System Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are CareerPath India's AI Career Mentor.

Your mission is to guide Indian students with practical and personalized career advice.

Always answer in simple language.

Your answer should include:

1. Career Overview
2. Why this career is suitable
3. Skills Required
4. Education Required
5. Best Indian Colleges
6. Government Opportunities
7. Private Opportunities
8. Certifications
9. Internship Suggestions
10. Expected Salary in India
11. Future Scope
12. Step-by-Step Learning Roadmap
13. Final Advice

Keep the answer professional and practical.

Maximum 400 words.
"""

# ==========================================================
# AI Career Mentor
# ==========================================================

def get_ai_guidance(question):

    prompt = f"""
{SYSTEM_PROMPT}

Student Question:

{question}
"""

    try:

        response = client.models.generate_content(
            model="models/gemini-3.6-flash",
            contents=prompt
        )

        if hasattr(response, "text"):
            return response.text

        return "Sorry, I couldn't generate a response."

    except Exception as e:

        print("Gemini Error:", e)

        return f"""
AI Service Error

{str(e)}

Please try again later.
"""