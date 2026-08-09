from models.career import Career
from extensions import db


def seed_careers():

    if Career.query.count() > 0:

        print("Careers already exist.")

        return

    careers = [

        {
            "title":"Software Engineer",
            "slug":"software-engineer",
            "category":"Technology",
            "description":"Develop software applications.",
            "average_salary":"₹8-25 LPA",
            "future_scope":"Excellent",
            "education_required":"B.Tech, BCA, MCA",
            "skills_required":"Python, Java, SQL"
        },

        {
            "title":"Data Scientist",
            "slug":"data-scientist",
            "category":"Technology",
            "description":"Analyze business data.",
            "average_salary":"₹10-30 LPA",
            "future_scope":"Excellent",
            "education_required":"B.Tech, MSc",
            "skills_required":"Python, ML, SQL"
        },

        {
            "title":"Cyber Security Analyst",
            "slug":"cyber-security-analyst",
            "category":"Technology",
            "description":"Protect computer systems.",
            "average_salary":"₹7-20 LPA",
            "future_scope":"Excellent",
            "education_required":"B.Tech",
            "skills_required":"Networking, Linux"
        },

        {
            "title":"AI Engineer",
            "slug":"ai-engineer",
            "category":"Technology",
            "description":"Build AI systems.",
            "average_salary":"₹12-40 LPA",
            "future_scope":"Excellent",
            "education_required":"B.Tech",
            "skills_required":"Python, TensorFlow"
        },

        {
            "title":"Doctor",
            "slug":"doctor",
            "category":"Medical",
            "description":"Medical professional.",
            "average_salary":"₹8-40 LPA",
            "future_scope":"Excellent",
            "education_required":"MBBS",
            "skills_required":"Medicine"
        },

        {
            "title":"IAS Officer",
            "slug":"ias-officer",
            "category":"Government",
            "description":"Civil Services.",
            "average_salary":"₹12-20 LPA",
            "future_scope":"Excellent",
            "education_required":"Graduation",
            "skills_required":"Leadership"
        },

        {
            "title":"IPS Officer",
            "slug":"ips-officer",
            "category":"Government",
            "description":"Police Service.",
            "average_salary":"₹12-20 LPA",
            "future_scope":"Excellent",
            "education_required":"Graduation",
            "skills_required":"Leadership"
        },

        {
            "title":"Chartered Accountant",
            "slug":"chartered-accountant",
            "category":"Business",
            "description":"Finance Professional.",
            "average_salary":"₹8-25 LPA",
            "future_scope":"Excellent",
            "education_required":"CA",
            "skills_required":"Accounting"
        }

    ]

    for item in careers:

        career = Career(**item)

        db.session.add(career)

    print(f"{len(careers)} careers inserted.")