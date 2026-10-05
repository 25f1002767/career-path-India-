import sqlite3

def migrate():
    con = sqlite3.connect('careerpathindia.db')
    cur = con.cursor()

    existing_cols = {col[1] for col in cur.execute('PRAGMA table_info(government_exams)').fetchall()}

    columns_to_add = [
        ('short_name', 'VARCHAR(100)'),
        ('exam_type', 'VARCHAR(100) DEFAULT "Recruitment"'),
        ('sub_category', 'VARCHAR(100)'),
        ('minimum_qualification', 'VARCHAR(100)'),
        ('streams', 'VARCHAR(250)'),
        ('age_min', 'INTEGER'),
        ('age_max', 'INTEGER'),
        ('eligibility', 'TEXT'),
        ('national_or_state', 'VARCHAR(50) DEFAULT "National"'),
        ('state', 'VARCHAR(100) DEFAULT "All India"'),
        ('region', 'VARCHAR(100)'),
        ('application_mode', 'VARCHAR(50) DEFAULT "Online"'),
        ('exam_mode', 'VARCHAR(100) DEFAULT "Computer Based Test (CBT)"'),
        ('selection_process', 'TEXT'),
        ('subjects', 'TEXT'),
        ('career_opportunities', 'TEXT'),
        ('related_courses', 'TEXT'),
        ('related_careers', 'TEXT'),
        ('application_url', 'VARCHAR(350)'),
        ('notification_url', 'VARCHAR(350)'),
        ('application_start_date', 'VARCHAR(100)'),
        ('application_end_date', 'VARCHAR(100)'),
        ('exam_date', 'VARCHAR(100)'),
        ('frequency', 'VARCHAR(100) DEFAULT "Annual"'),
        ('fee', 'VARCHAR(150)'),
        ('vacancies', 'VARCHAR(150)'),
        ('status', 'VARCHAR(50) DEFAULT "GENERAL_INFORMATION"'),
        ('source_url', 'VARCHAR(350)'),
        ('updated_at', 'DATETIME')
    ]

    added = 0
    for col_name, col_type in columns_to_add:
        if col_name not in existing_cols:
            cur.execute(f"ALTER TABLE government_exams ADD COLUMN {col_name} {col_type};")
            added += 1

    # Indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_exam_name ON government_exams(exam_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_exam_type ON government_exams(exam_type);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_exam_category ON government_exams(category);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_exam_state ON government_exams(state);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_exam_status ON government_exams(status);")

    con.commit()
    con.close()
    print(f"Migration completed. Added {added} columns and indexes.")

if __name__ == '__main__':
    migrate()
