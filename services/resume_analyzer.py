TECH_SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "flask",
    "django",
    "git",
    "github",
    "machine learning",
    "data science",
    "tensorflow",
    "power bi",
    "excel",
    "communication",
    "leadership",
    "problem solving"
]

CAREER_RULES = {

    "AI Engineer": [
        "python",
        "machine learning",
        "tensorflow",
        "sql"
    ],

    "Software Engineer": [
        "python",
        "java",
        "git",
        "sql"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "excel",
        "machine learning"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "flask"
    ]
}


def analyze_resume(text):

    text = text.lower()

    found = []

    # ----------------------------------
    # Detect Skills
    # ----------------------------------

    for skill in TECH_SKILLS:

        if skill in text:

            found.append(skill.title())

    # ----------------------------------
    # Calculate Score
    # ----------------------------------

    score = min(
        len(found) * 5,
        100
    )

    # ----------------------------------
    # Find Best Career
    # ----------------------------------

    best_career = "General Career"

    best_match = -1

    missing_skills = []

    for career, skills in CAREER_RULES.items():

        matched = 0

        missing = []

        for skill in skills:

            if skill in text:

                matched += 1

            else:

                missing.append(skill.title())

        if matched > best_match:

            best_match = matched

            best_career = career

            missing_skills = missing

    # ----------------------------------
    # Strengths & Weaknesses
    # ----------------------------------

    strengths = []

    weaknesses = []

    if score >= 80:

        strengths.append(
            "Strong technical profile"
        )

    else:

        weaknesses.append(
            "Need more technical skills"
        )

    if "communication" in text:

        strengths.append(
            "Communication Skills"
        )

    else:

        weaknesses.append(
            "Improve communication"
        )

    if "leadership" in text:

        strengths.append(
            "Leadership"
        )

    # ----------------------------------
    # Career Readiness
    # ----------------------------------

    readiness = "Beginner"

    if score >= 70:

        readiness = "Job Ready"

    elif score >= 40:

        readiness = "Intermediate"

    # ----------------------------------
    # Return Result
    # ----------------------------------

    return {

        "score": score,

        "career": best_career,

        "found": found,

        "missing_skills": missing_skills,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "ats_score": score,

        "readiness": readiness

    }