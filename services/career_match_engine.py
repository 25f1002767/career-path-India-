from models.career import Career


def calculate_match_score(context, career):

    score = 0

    reasons = []

    # Assessment Match
    if (
        context.get("recommended_category")
        and career.category == context["recommended_category"]
    ):

        score += 40

        reasons.append(
            "Matches your assessment category."
        )

    # Resume Match
    skills = (
        context.get("skills") or ""
    ).lower()

    career_skills = (
        career.skills_required or ""
    ).lower()

    matched = 0

    for skill in career_skills.split(","):

        skill = skill.strip()

        if skill and skill in skills:

            matched += 1

    score += matched * 8

    if matched:

        reasons.append(
            f"{matched} resume skills matched."
        )

    # Saved Career Bonus
    saved = context.get(
        "saved_careers",
        []
    )

    if career.title in saved:

        score += 15

        reasons.append(
            "Career saved by student."
        )

    score = min(score, 100)

    return score, reasons