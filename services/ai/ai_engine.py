from services.ai.context_builder import build_student_context
from services.ai.prompt_builder import build_prompt
from services.ai_career_mentor import get_ai_guidance


def ask_ai(user_id, question):

    context = build_student_context(user_id)

    prompt = build_prompt(
        context,
        question
    )

    return get_ai_guidance(prompt)