CAREERS = {

    "Python": "AI Engineer",

    "Machine Learning": "Data Scientist",

    "SQL": "Data Analyst",

    "Java": "Software Engineer",

    "Flask": "Backend Developer",

    "Communication": "Business Analyst"

}


def recommend(skills):

    careers = []

    for skill in skills:

        if skill in CAREERS:

            careers.append(CAREERS[skill])

    return list(set(careers))