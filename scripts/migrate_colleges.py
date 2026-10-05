import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "careerpathindia.db")

def migrate():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Inspect existing columns in 'colleges' table
    cursor.execute("PRAGMA table_info(colleges)")
    existing_cols = {row[1] for row in cursor.fetchall()}
    print(f"Existing columns in colleges table: {len(existing_cols)}")

    new_columns = [
        ("short_name", "VARCHAR(80)"),
        ("institution_type", "VARCHAR(100)"),
        ("institution_category", "VARCHAR(60) DEFAULT 'College'"),
        ("university_name", "VARCHAR(200)"),
        ("affiliated_university", "VARCHAR(200)"),
        ("address", "VARCHAR(350)"),
        ("district", "VARCHAR(100)"),
        ("pincode", "VARCHAR(20)"),
        ("latitude", "FLOAT"),
        ("longitude", "FLOAT"),
        ("government_private", "VARCHAR(50) DEFAULT 'Government'"),
        ("aided_unaided", "VARCHAR(50)"),
        ("autonomous", "BOOLEAN DEFAULT 0"),
        ("established_year", "INTEGER"),
        ("official_website", "VARCHAR(300)"),
        ("admission_url", "VARCHAR(300)"),
        ("contact_url", "VARCHAR(300)"),
        ("email", "VARCHAR(150)"),
        ("phone", "VARCHAR(100)"),
        ("recognition_status", "VARCHAR(150)"),
        ("ugc_status", "VARCHAR(60)"),
        ("aicte_status", "VARCHAR(60)"),
        ("accreditation", "VARCHAR(100)"),
        ("accreditation_grade", "VARCHAR(20)"),
        ("nirf_participation", "BOOLEAN DEFAULT 0"),
        ("nirf_category", "VARCHAR(80)"),
        ("nirf_rank", "INTEGER"),
        ("nirf_rank_year", "INTEGER"),
        ("source_url", "VARCHAR(350)"),
        ("updated_at", "DATETIME")
    ]

    added = 0
    for col_name, col_type in new_columns:
        if col_name not in existing_cols:
            alter_query = f"ALTER TABLE colleges ADD COLUMN {col_name} {col_type};"
            cursor.execute(alter_query)
            print(f"Added column: {col_name} ({col_type})")
            added += 1

    print(f"Migration completed for 'colleges': {added} new columns added.")

    # 2. Create 'courses' table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(150) NOT NULL UNIQUE,
            short_name VARCHAR(50),
            level VARCHAR(50),
            discipline VARCHAR(100),
            stream VARCHAR(100),
            duration VARCHAR(50),
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("Ensured 'courses' table exists.")

    # 3. Create 'college_courses' table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS college_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            college_id INTEGER NOT NULL REFERENCES colleges(id) ON DELETE CASCADE,
            course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
            admission_mode VARCHAR(120),
            eligibility VARCHAR(255),
            duration VARCHAR(50),
            specialization VARCHAR(150),
            fees_approx VARCHAR(100),
            source_url VARCHAR(350),
            verification_status VARCHAR(50) DEFAULT 'VERIFIED'
        );
    """)
    print("Ensured 'college_courses' table exists.")

    # 4. Create Indexes
    indexes = [
        ("idx_colleges_name", "CREATE INDEX IF NOT EXISTS idx_colleges_name ON colleges(name);"),
        ("idx_colleges_state", "CREATE INDEX IF NOT EXISTS idx_colleges_state ON colleges(state);"),
        ("idx_colleges_city", "CREATE INDEX IF NOT EXISTS idx_colleges_city ON colleges(city);"),
        ("idx_colleges_district", "CREATE INDEX IF NOT EXISTS idx_colleges_district ON colleges(district);"),
        ("idx_colleges_type", "CREATE INDEX IF NOT EXISTS idx_colleges_type ON colleges(institution_type);"),
        ("idx_colleges_gov_priv", "CREATE INDEX IF NOT EXISTS idx_colleges_gov_priv ON colleges(government_private);"),
        ("idx_colleges_status", "CREATE INDEX IF NOT EXISTS idx_colleges_status ON colleges(verification_status);"),
        ("idx_courses_name", "CREATE INDEX IF NOT EXISTS idx_courses_name ON courses(name);"),
        ("idx_courses_level", "CREATE INDEX IF NOT EXISTS idx_courses_level ON courses(level);"),
        ("idx_courses_discipline", "CREATE INDEX IF NOT EXISTS idx_courses_discipline ON courses(discipline);"),
        ("idx_cc_college_id", "CREATE INDEX IF NOT EXISTS idx_cc_college_id ON college_courses(college_id);"),
        ("idx_cc_course_id", "CREATE INDEX IF NOT EXISTS idx_cc_course_id ON college_courses(course_id);")
    ]

    for idx_name, sql in indexes:
        cursor.execute(sql)
        print(f"Verified index: {idx_name}")

    conn.commit()
    conn.close()
    print("College schema migration successfully finished!")

if __name__ == "__main__":
    migrate()
