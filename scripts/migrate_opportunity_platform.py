import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'careerpathindia.db')

def slugify(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def run_migration():
    print(f"Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Create opportunity_sources table
    print("Creating opportunity_sources table...")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS opportunity_sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        organisation VARCHAR(255) NOT NULL,
        source_type VARCHAR(100) DEFAULT 'Official Authority',
        authority_level VARCHAR(50) DEFAULT 'TIER_1_OFFICIAL',
        base_url VARCHAR(500) NOT NULL,
        official BOOLEAN DEFAULT 1,
        country VARCHAR(100) DEFAULT 'India',
        state VARCHAR(100) DEFAULT 'All India',
        category VARCHAR(100),
        active BOOLEAN DEFAULT 1,
        crawl_method VARCHAR(100) DEFAULT 'STATUTORY_FEED',
        api_available BOOLEAN DEFAULT 0,
        last_checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_success_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_failure_at DATETIME,
        parser_version VARCHAR(50) DEFAULT '1.0.0',
        robots_checked BOOLEAN DEFAULT 1,
        terms_review_status VARCHAR(50) DEFAULT 'REVIEWED_PERMITTED',
        health_status VARCHAR(50) DEFAULT 'HEALTHY',
        records_count INTEGER DEFAULT 0,
        notes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # 2. Create exam_cycles table
    print("Creating exam_cycles table...")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS exam_cycles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER NOT NULL,
        cycle_year INTEGER NOT NULL,
        cycle_name VARCHAR(200) NOT NULL,
        notification_number VARCHAR(150),
        notification_date VARCHAR(100),
        application_start_date VARCHAR(100),
        application_end_date VARCHAR(100),
        correction_date VARCHAR(100),
        admit_card_date VARCHAR(100),
        exam_date VARCHAR(100),
        result_date VARCHAR(100),
        counselling_date VARCHAR(100),
        interview_date VARCHAR(100),
        vacancies VARCHAR(150),
        application_fee VARCHAR(200),
        salary_or_stipend VARCHAR(150),
        status VARCHAR(50) DEFAULT 'UPCOMING',
        official_notification_url VARCHAR(500),
        official_application_url VARCHAR(500),
        admit_card_url VARCHAR(500),
        result_url VARCHAR(500),
        answer_key_url VARCHAR(500),
        cutoff_url VARCHAR(500),
        syllabus_url VARCHAR(500),
        previous_papers_url VARCHAR(500),
        source_id INTEGER,
        verification_status VARCHAR(50) DEFAULT 'VERIFIED_OFFICIAL',
        last_verified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (exam_id) REFERENCES government_exams(id) ON DELETE CASCADE,
        FOREIGN KEY (source_id) REFERENCES opportunity_sources(id) ON DELETE SET NULL
    );
    ''')

    # 3. Create student_opportunity_trackers table
    print("Creating student_opportunity_trackers table...")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS student_opportunity_trackers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        exam_id INTEGER NOT NULL,
        cycle_id INTEGER,
        status VARCHAR(50) DEFAULT 'Interested',
        application_number VARCHAR(100),
        target_score VARCHAR(50),
        notes TEXT,
        reminder_date VARCHAR(100),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (exam_id) REFERENCES government_exams(id) ON DELETE CASCADE,
        FOREIGN KEY (cycle_id) REFERENCES exam_cycles(id) ON DELETE SET NULL
    );
    ''')

    # 4. Create opportunity_change_logs table
    print("Creating opportunity_change_logs table...")
    cur.execute('''
    CREATE TABLE IF NOT EXISTS opportunity_change_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER NOT NULL,
        cycle_id INTEGER,
        field_name VARCHAR(100) NOT NULL,
        old_value TEXT,
        new_value TEXT,
        source VARCHAR(255),
        detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (exam_id) REFERENCES government_exams(id) ON DELETE CASCADE
    );
    ''')

    # 5. Check and add missing columns to government_exams
    existing_columns = [c[1] for c in cur.execute("PRAGMA table_info(government_exams);").fetchall()]
    new_cols = [
        ('slug', 'VARCHAR(250)'),
        ('full_name', 'VARCHAR(300)'),
        ('conducting_organisation', 'VARCHAR(300)'),
        ('organisation_type', "VARCHAR(100) DEFAULT 'Government'"),
        ('government_or_private', "VARCHAR(50) DEFAULT 'Government'"),
        ('central_or_state', "VARCHAR(50) DEFAULT 'Central'"),
        ('district', 'VARCHAR(100)'),
        ('opportunity_type', "VARCHAR(100) DEFAULT 'EXAM'"),
        ('education_level', 'VARCHAR(100)'),
        ('degree', 'VARCHAR(100)'),
        ('diploma', 'VARCHAR(100)'),
        ('specialisation', 'VARCHAR(250)'),
        ('preferred_qualification', 'VARCHAR(250)'),
        ('required_skills', 'TEXT'),
        ('age_relaxation', 'TEXT'),
        ('nationality', "VARCHAR(100) DEFAULT 'Indian'"),
        ('gender_eligibility', "VARCHAR(100) DEFAULT 'All'"),
        ('category_eligibility', "VARCHAR(200) DEFAULT 'General, OBC, SC, ST, EWS'"),
        ('pwd_eligibility', "VARCHAR(100) DEFAULT 'Eligible as per Govt Norms'"),
        ('domicile_requirement', "VARCHAR(200) DEFAULT 'None / All India'"),
        ('experience_requirement', "VARCHAR(200) DEFAULT 'Fresher / None'"),
        ('number_of_papers', 'VARCHAR(50)'),
        ('duration', 'VARCHAR(100)'),
        ('negative_marking', 'VARCHAR(100)'),
        ('admit_card_url', 'VARCHAR(500)'),
        ('result_url', 'VARCHAR(500)'),
        ('answer_key_url', 'VARCHAR(500)'),
        ('cutoff_url', 'VARCHAR(500)'),
        ('previous_papers_url', 'VARCHAR(500)'),
        ('syllabus_url', 'VARCHAR(500)'),
        ('calendar_url', 'VARCHAR(500)'),
        ('source_id', 'INTEGER'),
        ('url_status', "VARCHAR(50) DEFAULT 'VALID'")
    ]

    for col_name, col_def in new_cols:
        if col_name not in existing_columns:
            print(f"Adding column {col_name} to government_exams...")
            cur.execute(f"ALTER TABLE government_exams ADD COLUMN {col_name} {col_def};")

    # Populate slugs for existing exams if empty
    exams = cur.execute("SELECT id, exam_name, short_name FROM government_exams;").fetchall()
    for eid, ename, eshort in exams:
        base_slug = slugify(eshort if eshort else ename)
        unique_slug = f"{base_slug}-{eid}"
        cur.execute("UPDATE government_exams SET slug = ? WHERE id = ? AND (slug IS NULL OR slug = '');", (unique_slug, eid))

    # Commit transactions
    conn.commit()
    conn.close()
    print("Database migration completed successfully!")

if __name__ == '__main__':
    run_migration()
