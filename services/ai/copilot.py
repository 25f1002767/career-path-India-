from services.ai.context_builder import build_student_context
from services.recommendation_engine import recommend_best_careers
from services.roadmap_engine import generate_roadmap
from services.ai.prompt_builder import build_prompt
from services.ai_career_mentor import get_ai_guidance


def career_copilot(user_id, question):

    context = build_student_context(user_id)

    recommendations = recommend_best_careers(context)

    roadmap = None

    if recommendations:

        roadmap = generate_roadmap(
            recommendations[0]["career"]
        )

        context["top_career"] = recommendations[0]["career"].title
        context["career_score"] = recommendations[0]["score"]
        context["roadmap"] = roadmap

    prompt = build_prompt(
        context,
        question
    )

    return get_ai_guidance(prompt)