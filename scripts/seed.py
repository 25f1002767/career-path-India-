import csv
import os
import sys

# Add project root to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from app import app
from extensions import db
from models.career import Career

CAREERS_CSV = os.path.join(
    BASE_DIR,
    "data",
    "careers.csv"
)

def seed_careers():

    with app.app_context():

        Career.query.delete()

        db.session.commit()

        with open(
            CAREERS_CSV,
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                career = Career(

                    title=row["title"],

                    slug=row["slug"],

                    category=row["category"],

                    description=row["description"],

                    average_salary=row["average_salary"],

                    future_scope=row["future_scope"],

                    education_required=row["education_required"],

                    skills_required=row["skills_required"],

                    icon="briefcase"

                )

                db.session.add(career)

            db.session.commit()

            print("✅ Careers Imported Successfully")


if __name__ == "__main__":

    seed_careers()