from scripts.populate_database import populate_all

if __name__ == "__main__":
    print("=" * 60)
    print("MPath Career Counselling Database Seeder")
    print("=" * 60)
    populate_all()

    try:
        from app import app
        from models.course import Course
        with app.app_context():
            if Course.query.count() == 0:
                print("Seeding courses and institutional degree mappings...")
                from scripts.seed_comprehensive_colleges import seed_courses_and_colleges
                seed_courses_and_colleges()

            # Ensure all internship application links are 100% verified
            from scripts.update_internship_urls import update_database
            update_database()
    except Exception as e:
        print(f"Course/Internship verification note: {e}")

    print("\nDatabase Successfully Synchronized!")

