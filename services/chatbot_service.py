from services.ai_career_mentor import get_ai_guidance


def ask_ai(prompt):
    if not prompt or not prompt.strip():
        return "Please ask a question regarding your career, college, exam, or skills."
    return get_ai_guidance(prompt.strip())