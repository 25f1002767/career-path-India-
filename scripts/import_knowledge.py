import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT))

from app import app
from extensions import db
from models.career import Career

BASE = (
    Path(__file__)
    .resolve()
    .parents[1]
    / "knowledge"
    / "1"
    / "careers"
)


with app.app_context():

    Career.query.delete()

    db.session.commit()

    count = 0

    for file in BASE.rglob("*.json"):

        if "template" in file.name.lower():
            continue

        if "schema" in file.name.lower():
            continue

        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            career = Career(

                title=data.get("title"),

                slug=data.get(
                    "title",
                    ""
                ).lower().replace(" ", "-"),

                category=data.get(
                    "category",
                    "Technology"
                ),

                description=data.get(
                    "overview",
                    ""
                ),

                average_salary=data.get(
                    "salary",
                    {}
                ).get(
                    "entry",
                    ""
                ),

                future_scope=data.get(
                    "future_scope",
                    ""
                )

            )

            db.session.add(career)

            count += 1

        except Exception as e:

            print(file)

            print(e)

    db.session.commit()

    print()

    print("=" * 40)

    print("Imported Careers:", count)

    print("=" * 40)