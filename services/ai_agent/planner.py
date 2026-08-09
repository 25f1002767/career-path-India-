def create_plan(question):

    plan = []

    question = question.lower()

    if "career" in question:

        plan.append("career")

    if "college" in question:

        plan.append("college")

    if "scholarship" in question:

        plan.append("scholarship")

    if "resume" in question:

        plan.append("resume")

    if "roadmap" in question:

        plan.append("roadmap")

    if "internship" in question:

        plan.append("internship")

    return plan