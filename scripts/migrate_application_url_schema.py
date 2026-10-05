"""
scripts/migrate_application_url_schema.py
Safely upgrades 'scholarships' and 'scholarship_cycles' with segregated URL fields,
validation statuses, and creates 'scholarship_application_clicks' table.
"""

import sqlite3

def run_migration():
    conn = sqlite3.connect("careerpathindia.db")
    c = conn.cursor()

    def add_col(table, col, col_type):
        cols = [r[1] for r in c.execute(f"PRAGMA table_info({table})").fetchall()]
        if col not in cols:
            print(f"Adding column '{col}' to table '{table}'...")
            c.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")

    # 1. Scholarships table updates
    add_col("scholarships", "application_url_status", "TEXT DEFAULT 'VALID'")
    add_col("scholarships", "application_url_last_checked", "DATETIME")
    add_col("scholarships", "application_url_verified_at", "DATETIME")
    add_col("scholarships", "application_url_verified_by", "TEXT")
    add_col("scholarships", "final_application_url", "TEXT")
    add_col("scholarships", "official_website", "TEXT")
    add_col("scholarships", "notification_url", "TEXT")

    # 2. Scholarship Cycles table updates
    add_col("scholarship_cycles", "official_application_url", "TEXT")
    add_col("scholarship_cycles", "official_website", "TEXT")
    add_col("scholarship_cycles", "faq_url", "TEXT")
    add_col("scholarship_cycles", "application_url_status", "TEXT DEFAULT 'VALID'")

    # 3. Create Scholarship Application Clicks table for audit analytics
    c.execute("""
    CREATE TABLE IF NOT EXISTS scholarship_application_clicks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scholarship_id INTEGER NOT NULL,
        user_id INTEGER,
        cycle_id INTEGER,
        target_url TEXT NOT NULL,
        click_source TEXT DEFAULT 'direct',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY(cycle_id) REFERENCES scholarship_cycles(id) ON DELETE SET NULL
    )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_sch_clicks_sch_id ON scholarship_application_clicks(scholarship_id)")

    conn.commit()
    conn.close()
    print("Schema migration for application URLs and clicks completed successfully.")

if __name__ == "__main__":
    run_migration()
