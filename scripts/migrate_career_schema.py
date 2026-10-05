import sqlite3
import os

DB_PATH = "careerpathindia.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Inspect existing columns in careers
    cursor.execute("PRAGMA table_info(careers)")
    existing_cols = {row[1] for row in cursor.fetchall()}
    print(f"Existing career columns: {len(existing_cols)}")

    new_career_cols = [
        ("short_name", "VARCHAR(100)"),
        ("sub_category", "VARCHAR(100)"),
        ("industry", "VARCHAR(100)"),
        ("short_description", "TEXT"),
        ("what_they_do", "TEXT"),
        ("day_to_day_work", "TEXT"),
        ("work_modes", "VARCHAR(150)"),
        ("minimum_qualification", "VARCHAR(100)"),
        ("preferred_streams", "VARCHAR(255)"),
        ("required_subjects", "VARCHAR(255)"),
        ("technical_skills", "TEXT"),
        ("soft_skills", "TEXT"),
        ("tools", "TEXT"),
        ("career_progression", "TEXT"),
        ("entry_routes", "TEXT"),
        ("higher_study_options", "TEXT"),
        ("entrepreneurship_options", "TEXT"),
        ("internship_roles", "TEXT"),
        ("entry_level_roles", "TEXT"),
        ("salary_indicative", "TEXT"),
        ("updated_at", "DATETIME")
    ]

    for col_name, col_type in new_career_cols:
        if col_name not in existing_cols:
            print(f"Adding column '{col_name}' to careers...")
            cursor.execute(f"ALTER TABLE careers ADD COLUMN {col_name} {col_type}")

    # 2. Inspect career_skills
    cursor.execute("PRAGMA table_info(career_skills)")
    skill_cols = {row[1] for row in cursor.fetchall()}
    if "skill_category" not in skill_cols:
        print("Adding skill_category to career_skills...")
        cursor.execute("ALTER TABLE career_skills ADD COLUMN skill_category VARCHAR(50)")
    if "importance" not in skill_cols:
        print("Adding importance to career_skills...")
        cursor.execute("ALTER TABLE career_skills ADD COLUMN importance VARCHAR(50)")

    # 3. Inspect career_roadmaps
    cursor.execute("PRAGMA table_info(career_roadmaps)")
    roadmap_cols = {row[1] for row in cursor.fetchall()}
    if "path_name" not in roadmap_cols:
        print("Adding path_name to career_roadmaps...")
        cursor.execute("ALTER TABLE career_roadmaps ADD COLUMN path_name VARCHAR(150)")
    if "path_type" not in roadmap_cols:
        print("Adding path_type to career_roadmaps...")
        cursor.execute("ALTER TABLE career_roadmaps ADD COLUMN path_type VARCHAR(50)")
    if "starting_point" not in roadmap_cols:
        print("Adding starting_point to career_roadmaps...")
        cursor.execute("ALTER TABLE career_roadmaps ADD COLUMN starting_point VARCHAR(100)")

    # 4. Create career_courses table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        career_id INTEGER NOT NULL REFERENCES careers(id) ON DELETE CASCADE,
        course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
        relationship_type VARCHAR(50) DEFAULT 'COMMON',
        description VARCHAR(255),
        source_url VARCHAR(350),
        verification_status VARCHAR(50) DEFAULT 'VERIFIED'
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_career_courses_career ON career_courses(career_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_career_courses_course ON career_courses(course_id)")

    # 5. Create career_exams table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        career_id INTEGER NOT NULL REFERENCES careers(id) ON DELETE CASCADE,
        exam_id INTEGER NOT NULL REFERENCES government_exams(id) ON DELETE CASCADE,
        importance VARCHAR(50) DEFAULT 'PRIMARY',
        eligibility_summary VARCHAR(255),
        verification_status VARCHAR(50) DEFAULT 'VERIFIED'
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_career_exams_career ON career_exams(career_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_career_exams_exam ON career_exams(exam_id)")

    conn.commit()
    conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
