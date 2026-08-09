import json
from pathlib import Path
from copy import deepcopy

BASE_PATH = (
    Path(__file__).resolve().parents[1]
    / "knowledge"
    / "1"
    / "careers"
    / "technology"
)

BASE_PATH.mkdir(parents=True, exist_ok=True)

# Load AI Engineer template
with open(
    BASE_PATH / "01_ai_engineer.json",
    "r",
    encoding="utf-8"
) as f:
    template = json.load(f)

careers = [

    {
        "id": 2,
        "title": "Software Engineer",
        "salary": "₹4–8 LPA"
    },

    {
        "id": 3,
        "title": "Data Scientist",
        "salary": "₹6–12 LPA"
    },

    {
        "id": 4,
        "title": "Machine Learning Engineer",
        "salary": "₹8–15 LPA"
    },

    {
        "id": 5,
        "title": "Cloud Engineer",
        "salary": "₹6–14 LPA"
    },

    {
        "id": 6,
        "title": "DevOps Engineer",
        "salary": "₹6–14 LPA"
    },

    {
        "id": 7,
        "title": "Cyber Security Engineer",
        "salary": "₹5–12 LPA"
    },

    {
        "id": 8,
        "title": "Backend Developer",
        "salary": "₹5–10 LPA"
    },

    {
        "id": 9,
        "title": "Frontend Developer",
        "salary": "₹4–9 LPA"
    },

    {
        "id": 10,
        "title": "Full Stack Developer",
        "salary": "₹6–12 LPA"
    }

]

for career in careers:

    data = deepcopy(template)

    data["id"] = career["id"]

    data["title"] = career["title"]

    data["slug"] = (
        career["title"]
        .lower()
        .replace(" ", "-")
    )

    data["summary"] = (
        f"{career['title']} is one of the fastest growing technology careers."
    )

    data["description"] = (
        f"A {career['title']} designs, develops, and maintains modern software solutions for businesses and users."
    )

    data["average_salary"]["fresher"] = career["salary"]

    filename = (
        f"{career['id']:02d}_"
        + data["slug"]
        + ".json"
    )

    with open(
        BASE_PATH / filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

print()
print("=" * 50)
print("Technology Careers Generated Successfully")
print("=" * 50)