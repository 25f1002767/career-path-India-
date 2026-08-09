import json
from pathlib import Path

BASE_PATH = (
    Path(__file__)
    .resolve()
    .parents[1]
    / "knowledge"
    / "1"
    / "careers"
    / "technology"
)

BASE_PATH.mkdir(
    parents=True,
    exist_ok=True
)

careers = [

    {
        "file":"02_software_engineer.json",
        "title":"Software Engineer"
    },

    {
        "file":"03_data_scientist.json",
        "title":"Data Scientist"
    },

    {
        "file":"04_ml_engineer.json",
        "title":"Machine Learning Engineer"
    },

    {
        "file":"05_cloud_engineer.json",
        "title":"Cloud Engineer"
    },

    {
        "file":"06_devops_engineer.json",
        "title":"DevOps Engineer"
    },

    {
        "file":"07_cyber_security.json",
        "title":"Cyber Security Engineer"
    },

    {
        "file":"08_backend_developer.json",
        "title":"Backend Developer"
    },

    {
        "file":"09_frontend_developer.json",
        "title":"Frontend Developer"
    },

    {
        "file":"10_full_stack_developer.json",
        "title":"Full Stack Developer"
    }

]

for career in careers:

    data = {

        "title": career["title"],

        "category": "Technology",

        "overview": f"{career['title']} is one of the fastest growing careers in technology.",

        "required_skills":[

            "Communication",

            "Problem Solving"

        ],

        "salary":{

            "entry":"4-8 LPA",

            "mid":"10-18 LPA",

            "senior":"20+ LPA"

        },

        "future_scope":"Excellent",

        "roadmap":[

            "Learn Fundamentals",

            "Build Projects",

            "Internship",

            "Get Job"

        ]

    }

    with open(

        BASE_PATH / career["file"],

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            indent=4

        )

print("Technology careers generated successfully.")