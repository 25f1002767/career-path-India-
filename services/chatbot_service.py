from services.ai_client import client


def ask_ai(prompt):

    # If API key is missing
    if client is None:

        return (
            "🤖 AI assistant is temporarily unavailable. "
            "Please try again later."
        )

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception:

        return (
            "⚠️ Unable to connect to Gemini AI right now."
        )