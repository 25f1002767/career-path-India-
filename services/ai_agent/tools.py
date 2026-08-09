from services.ai.context_builder import build_student_context
from services.recommendation_engine import recommend_best_careers


def career_tool(user_id):

    context = build_student_context(user_id)

    return recommend_best_careers(context)


def resume_tool(user_id):

    context = build_student_context(user_id)

    return context


def roadmap_tool():

    return "Roadmap Generated"


def scholarship_tool():

    return "Scholarship Suggestions"


def college_tool():

    return "College Suggestions"


def internship_tool():

    return "Internship Suggestions"