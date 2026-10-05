import sqlite3

def migrate():
    conn = sqlite3.connect('careerpathindia.db')
    cur = conn.cursor()
    existing_cols = [c[1] for c in cur.execute('PRAGMA table_info(assessment_results);').fetchall()]
    new_cols = [
        ('assessment_version', 'VARCHAR(20) DEFAULT "2.0.0"'),
        ('confidence_level', 'VARCHAR(50) DEFAULT "HIGH_CONFIDENCE"'),
        ('summary_headline', 'VARCHAR(255)'),
        ('answers_json', 'TEXT'),
        ('profile_json', 'TEXT'),
        ('recommendations_json', 'TEXT'),
        ('unexpected_json', 'TEXT'),
        ('tradeoffs_json', 'TEXT'),
        ('actions_json', 'TEXT')
    ]
    added = []
    for name, col_type in new_cols:
        if name not in existing_cols:
            cur.execute(f"ALTER TABLE assessment_results ADD COLUMN {name} {col_type};")
            added.append(name)
    conn.commit()
    all_cols = [c[1] for c in cur.execute('PRAGMA table_info(assessment_results);').fetchall()]
    conn.close()
    print("Added columns:", added)
    print("All assessment_results columns now:", all_cols)

if __name__ == "__main__":
    migrate()
