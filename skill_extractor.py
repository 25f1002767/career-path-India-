SKILLS = [

    "Python",
    "Java",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Flask",
    "Machine Learning",
    "Data Science",
    "Git",
    "Linux",
    "Power BI",
    "Excel",
    "Communication",
    "Leadership"

]


def extract_skills(text):

    found = []

    lower = text.lower()

    for skill in SKILLS:

        if skill.lower() in lower:

            found.append(skill)

    return found