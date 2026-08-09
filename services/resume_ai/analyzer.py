from services.resume_ai.skill_extractor import extract_skills
from services.resume_ai.ats_score import calculate_ats_score
from services.resume_ai.recommendation import recommend


def analyze_resume(text):

    skills = extract_skills(text)

    score = calculate_ats_score(skills)

    careers = recommend(skills)

    return {

        "score": score,

        "skills": skills,

        "recommended": careers

    }