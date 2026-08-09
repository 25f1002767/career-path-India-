from app import app
from extensions import db

from seed_data.careers_seed import seed_careers
from seed_data.exams_seed import seed_exams
from seed_data.scholarships_seed import seed_scholarships
from seed_data.internships_seed import seed_internships
from seed_data.colleges_seed import seed_colleges


with app.app_context():

    print("=" * 60)
    print("CareerPath India Database Seeder")
    print("=" * 60)

    seed_careers()

    seed_exams()

    seed_scholarships()

    seed_internships()

    seed_colleges()

    db.session.commit()

    print("\nDatabase Successfully Seeded!")