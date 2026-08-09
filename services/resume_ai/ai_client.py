from services.ai_client import client

if client:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text

else:

    text = "AI service temporarily unavailable."