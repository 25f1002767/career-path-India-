def analyze_skill_gap(career, user_skills):

    required = []

    # -----------------------------
    # JSON dictionary support
    # -----------------------------

    skills_data = career.get("skills", {})

    required = skills_data.get("technical", [])

    # -----------------------------
    # Normalize user skills
    # -----------------------------

    user = [

        skill.strip().lower()

        for skill in user_skills

    ]

    matched = []
    missing = []

    for skill in required:

        if skill.lower() in user:

            matched.append(skill)

        else:

            missing.append(skill)

    # -----------------------------
    # Calculate percentage
    # -----------------------------

    if len(required) == 0:

        percentage = 0

    else:

        percentage = round(

            len(matched)

            / len(required)

            * 100,

            1

        )

    return {

        "matched": matched,

        "missing": missing,

        "percentage": percentage

    }