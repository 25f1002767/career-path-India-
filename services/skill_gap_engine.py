def find_skill_gap(context, career):

    resume = (
        context.get("skills") or ""
    ).lower()

    required = (
        career.skills_required or ""
    ).split(",")

    missing = []

    for skill in required:

        skill = skill.strip()

        if skill.lower() not in resume:

            missing.append(skill)

    return missing