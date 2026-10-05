"""
scripts/migrate_scholarship_schema.py
==============================================================================
MPath National Scholarship Platform - Database Schema Migration
==============================================================================
Safely alters existing 'scholarships' table and creates:
- scholarship_cycles
- scholarship_applications
- scholarship_fields
- student_documents
- scholarship_application_documents
==============================================================================
"""

import sqlite3
import re
import os

DB_PATH = "careerpathindia.db"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[\(\)\[\]\{\}]', '', text)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:200]

def migrate():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Inspect existing columns in 'scholarships'
    existing_cols = {col[1] for col in c.execute("PRAGMA table_info(scholarships)").fetchall()}
    print(f"Existing columns in 'scholarships': {len(existing_cols)}")

    new_columns = [
        ("slug", "TEXT"),
        ("short_title", "TEXT"),
        ("provider_name", "TEXT"),
        ("provider_type", "TEXT"),
        ("ministry", "TEXT"),
        ("department", "TEXT"),
        ("organization", "TEXT"),
        ("short_description", "TEXT"),
        ("objective", "TEXT"),
        ("scholarship_type", "TEXT"),
        ("national_or_state", "TEXT DEFAULT 'National'"),
        ("district", "TEXT"),
        ("education_level", "TEXT"),
        ("minimum_qualification", "TEXT"),
        ("maximum_qualification", "TEXT"),
        ("streams", "TEXT"),
        ("courses", "TEXT"),
        ("sub_category", "TEXT"),
        ("gender_eligibility", "TEXT DEFAULT 'All'"),
        ("age_min", "INTEGER"),
        ("age_max", "INTEGER"),
        ("family_income_limit", "REAL"),
        ("percentage_requirement", "REAL"),
        ("academic_requirement", "TEXT"),
        ("category_requirement", "TEXT DEFAULT 'All'"),
        ("disability_requirement", "TEXT DEFAULT 'None'"),
        ("domicile_requirement", "TEXT"),
        ("benefit_type", "TEXT"),
        ("amount_description", "TEXT"),
        ("tuition_fee_support", "TEXT"),
        ("maintenance_allowance", "TEXT"),
        ("hostel_support", "TEXT"),
        ("book_allowance", "TEXT"),
        ("duration", "TEXT"),
        ("renewable", "BOOLEAN DEFAULT 1"),
        ("number_of_awards", "TEXT"),
        ("selection_process", "TEXT"),
        ("application_mode", "TEXT DEFAULT 'Online - National Scholarship Portal (NSP)'"),
        ("official_application_url", "TEXT"),
        ("guidelines_url", "TEXT"),
        ("faq_url", "TEXT"),
        ("application_method", "TEXT DEFAULT 'EXTERNAL_PORTAL'"),
        ("requires_otr", "BOOLEAN DEFAULT 0"),
        ("requires_institute_verification", "BOOLEAN DEFAULT 1"),
        ("requires_nodal_verification", "BOOLEAN DEFAULT 0"),
        ("documents_required", "TEXT"),
        ("common_mistakes", "TEXT"),
        ("faqs", "TEXT"),
        ("renewal_rules", "TEXT"),
        ("updated_at", "DATETIME")
    ]

    for col_name, col_type in new_columns:
        if col_name not in existing_cols:
            print(f"Adding column '{col_name}' ({col_type}) to 'scholarships'...")
            c.execute(f"ALTER TABLE scholarships ADD COLUMN {col_name} {col_type}")

    # Create index on slug if not exists
    c.execute("CREATE INDEX IF NOT EXISTS idx_scholarships_slug ON scholarships(slug)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_scholarships_state ON scholarships(state)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_scholarships_provider_type ON scholarships(provider_type)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_scholarships_education_level ON scholarships(education_level)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_scholarships_category ON scholarships(category)")

    # 2. Create 'scholarship_cycles' table
    c.execute("""
    CREATE TABLE IF NOT EXISTS scholarship_cycles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scholarship_id INTEGER NOT NULL,
        academic_year TEXT NOT NULL,
        application_start_date TEXT,
        application_end_date TEXT,
        correction_start_date TEXT,
        correction_end_date TEXT,
        verification_deadline TEXT,
        result_date TEXT,
        disbursement_date TEXT,
        status TEXT DEFAULT 'OPEN',
        amount TEXT,
        vacancies_or_slots TEXT,
        notification_url TEXT,
        guidelines_url TEXT,
        source_url TEXT,
        verification_status TEXT DEFAULT 'VERIFIED',
        last_verified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
    )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_cycles_scholarship_id ON scholarship_cycles(scholarship_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_cycles_status ON scholarship_cycles(status)")

    # 3. Create 'scholarship_applications' table
    c.execute("""
    CREATE TABLE IF NOT EXISTS scholarship_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        scholarship_id INTEGER NOT NULL,
        cycle_id INTEGER,
        application_number TEXT UNIQUE,
        external_reference_number TEXT,
        status TEXT DEFAULT 'DRAFT',
        submission_type TEXT DEFAULT 'EXTERNAL_PORTAL_PREPARED',
        progress_percent INTEGER DEFAULT 15,
        form_data TEXT,
        eligibility_snapshot TEXT,
        student_notes TEXT,
        user_declared_status TEXT,
        user_declared_status_updated_at DATETIME,
        submitted_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE,
        FOREIGN KEY (cycle_id) REFERENCES scholarship_cycles(id) ON DELETE SET NULL
    )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_applications_user_id ON scholarship_applications(user_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_applications_scholarship_id ON scholarship_applications(scholarship_id)")

    # 4. Create 'scholarship_fields' table
    c.execute("""
    CREATE TABLE IF NOT EXISTS scholarship_fields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scholarship_id INTEGER,
        field_name TEXT NOT NULL,
        label TEXT NOT NULL,
        field_type TEXT NOT NULL,
        required BOOLEAN DEFAULT 1,
        validation_rule TEXT,
        options TEXT,
        help_text TEXT,
        section TEXT NOT NULL,
        "order" INTEGER DEFAULT 0,
        sensitive BOOLEAN DEFAULT 0,
        autofill_source TEXT,
        FOREIGN KEY (scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
    )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_fields_scholarship_id ON scholarship_fields(scholarship_id)")

    # 5. Create 'student_documents' table (Document Vault)
    c.execute("""
    CREATE TABLE IF NOT EXISTS student_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        document_type TEXT NOT NULL,
        document_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER DEFAULT 0,
        mime_type TEXT,
        verification_status TEXT DEFAULT 'UPLOADED',
        notes TEXT,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_docs_user_id ON student_documents(user_id)")

    # 6. Create 'scholarship_application_documents' table
    c.execute("""
    CREATE TABLE IF NOT EXISTS scholarship_application_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER NOT NULL,
        document_id INTEGER,
        document_type TEXT NOT NULL,
        document_label TEXT NOT NULL,
        is_mandatory BOOLEAN DEFAULT 1,
        status TEXT DEFAULT 'PENDING',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (application_id) REFERENCES scholarship_applications(id) ON DELETE CASCADE,
        FOREIGN KEY (document_id) REFERENCES student_documents(id) ON DELETE SET NULL
    )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_app_docs_app_id ON scholarship_application_documents(application_id)")

    # 7. Update slugs and provider types for existing 20 records
    existing_rows = c.execute("SELECT id, title, provider, state FROM scholarships").fetchall()
    for row_id, title, provider, state in existing_rows:
        slug = slugify(title)
        # Ensure unique slug
        clash = c.execute("SELECT id FROM scholarships WHERE slug = ? AND id != ?", (slug, row_id)).fetchone()
        if clash:
            slug = f"{slug}-{row_id}"

        prov_type = "Central Government"
        if "AICTE" in (provider or ""):
            prov_type = "UGC / AICTE"
        elif "UGC" in (provider or ""):
            prov_type = "UGC / AICTE"
        elif state and state != "All India" and state != "All":
            prov_type = "State Government"

        c.execute("""
            UPDATE scholarships 
            SET slug = ?,
                provider_name = COALESCE(provider_name, provider),
                provider_type = COALESCE(provider_type, ?),
                official_application_url = COALESCE(official_application_url, website, official_url, 'https://scholarships.gov.in')
            WHERE id = ?
        """, (slug, prov_type, row_id))

        # Check if cycle exists for this scholarship
        cyc = c.execute("SELECT id FROM scholarship_cycles WHERE scholarship_id = ?", (row_id,)).fetchone()
        if not cyc:
            c.execute("""
                INSERT INTO scholarship_cycles (
                    scholarship_id, academic_year, application_start_date, application_end_date,
                    status, verification_status, source_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row_id,
                "2026-27",
                "01-Jul-2026",
                "31-Oct-2026",
                "OPEN",
                "VERIFIED",
                "https://scholarships.gov.in"
            ))

    conn.commit()
    conn.close()
    print("Schema migration completed successfully!")

if __name__ == "__main__":
    migrate()
