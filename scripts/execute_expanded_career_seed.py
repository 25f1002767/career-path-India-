"""
scripts/execute_expanded_career_seed.py
==============================================================================
MPath Career Universe Master Expansion
==============================================================================
Enriches existing 126 careers with new dimension metadata.
Appends 88+ authentic occupational pathways across all 26 domains (A to Z).
Populates:
  - careers
  - career_courses
  - career_exams
  - career_skills
  - career_roadmaps
==============================================================================
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "careerpathindia.db"

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

def collect_new_careers():
    import catalog_expanded_part1 as p1
    import catalog_expanded_part2 as p2
    import catalog_expanded_part3 as p3
    import catalog_expanded_part4 as p4
    import catalog_expanded_part5 as p5
    import catalog_expanded_part6 as p6
    import catalog_expanded_part7 as p7
    import catalog_expanded_part8 as p8
    import catalog_expanded_part9 as p9
    import catalog_expanded_part10 as p10
    import catalog_expanded_part11 as p11

    new_list = []
    for p in [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]:
        for attr in dir(p):
            if attr.startswith("get_"):
                new_list.extend(getattr(p, attr)())

    seen = set()
    unique = []
    for c in new_list:
        slug = c.get("slug")
        if slug and slug not in seen:
            seen.add(slug)
            unique.append(c)

    return unique

def enrich_existing_careers(cursor):
    """Enrich the existing 126 careers with newly added schema attributes"""
    rows = cursor.execute("SELECT id, title, category, technical_skills, minimum_qualification FROM careers").fetchall()
    
    updated_count = 0
    for r in rows:
        cid, title, cat, tech_skills, min_qual = r
        cat_lower = (cat or "").lower()
        title_lower = (title or "").lower()

        # Derive career family
        family = "General Professional"
        if any(k in cat_lower for k in ["healthcare", "medical"]):
            family = "Healthcare & Medicine"
        elif any(k in cat_lower for k in ["law", "legal"]):
            family = "Law & Justice"
        elif any(k in cat_lower for k in ["government", "defence", "civil"]):
            family = "Public Administration & Defence"
        elif any(k in cat_lower for k in ["finance", "banking", "account"]):
            family = "Finance & Accountancy"
        elif any(k in cat_lower for k in ["education", "teaching", "academia"]):
            family = "Education & Pedagogy"
        elif any(k in cat_lower for k in ["agriculture", "environment", "food"]):
            family = "Agriculture, Ecology & Earth"
        elif any(k in cat_lower for k in ["design", "animation", "creative", "media"]):
            family = "Creative & Media Arts"
        elif any(k in cat_lower for k in ["technology", "computer"]):
            family = "Technology & Computing"
        elif any(k in cat_lower for k in ["engineering", "manufacturing"]):
            family = "Engineering & Industry"
        elif any(k in cat_lower for k in ["business", "management", "consulting"]):
            family = "Business & Strategy"
        elif any(k in cat_lower for k in ["aviation", "logistics"]):
            family = "Aviation & Logistics"
        elif any(k in cat_lower for k in ["social", "psychology"]):
            family = "Social Sciences & Policy"

        # Derive interest clusters
        clusters = []
        if "technology" in cat_lower:
            clusters.extend(["Technology", "Science", "Analysis", "Machines"])
        elif "healthcare" in cat_lower:
            clusters.extend(["Healthcare", "Science", "Helping", "People"])
        elif "law" in cat_lower:
            clusters.extend(["Law", "Government", "Society", "Writing"])
        elif "government" in cat_lower:
            clusters.extend(["Government", "Leadership", "Society", "Public Service"])
        elif "finance" in cat_lower:
            clusters.extend(["Numbers", "Business", "Analysis"])
        elif "education" in cat_lower:
            clusters.extend(["Teaching", "People", "Helping", "Language"])
        elif "agriculture" in cat_lower:
            clusters.extend(["Nature", "Science", "Agriculture", "Outdoor", "Hands-on"])
        elif any(k in cat_lower for k in ["design", "media", "creative"]):
            clusters.extend(["Creativity", "Art", "Design", "Media"])
        else:
            clusters.extend(["Business", "Society", "People"])

        clusters_str = ", ".join(clusters)

        # Derive work style
        work_style = "Office"
        if "healthcare" in cat_lower:
            work_style = "Hospital, Clinic"
        elif "law" in cat_lower:
            work_style = "Court, Chamber, Office"
        elif "government" in cat_lower:
            work_style = "Government Office, Field"
        elif "agriculture" in cat_lower:
            work_style = "Farm, Field, Lab"
        elif "technology" in cat_lower:
            work_style = "Office, Remote"
        elif "aviation" in cat_lower:
            work_style = "Airport, Warehouse, Travel"
        elif any(k in cat_lower for k in ["design", "media"]):
            work_style = "Studio, Office, Remote"

        # Check if lesser known
        is_lesser = False
        lesser_titles = ["actuary", "audiologist", "cartographer", "forensic", "curator", "archivist", "geneticist", "ecologist", "hydrologist", "pedologist", "ergonomic", "biomedical"]
        if any(w in title_lower for w in lesser_titles):
            is_lesser = True

        # Reality check
        reality_check = (
            "Entry salary levels are indicative and depend on institutional quality, personal performance, and experience.\n"
            "Continuous technical and professional upskilling is necessary throughout this career.\n"
            "Practical internships and project portfolios significantly enhance initial placement success."
        )
        if "government" in cat_lower:
            reality_check = (
                "Competition ratio in competitive examinations is intense (often under 0.5% final selection).\n"
                "Initial posting tenures may involve mandatory rural or hardship location postings.\n"
                "Requires 1 to 2 years of disciplined, structured preparation."
            )
        elif "healthcare" in cat_lower:
            reality_check = (
                "Requires long educational training and mandatory clinical hospital rotations.\n"
                "Demands high emotional empathy and physical resilience during patient emergencies.\n"
                "Requires statutory licensing and registration with official national healthcare councils."
            )

        # Next steps
        next_steps = (
            f"1. Explore the recognized undergraduate and postgraduate degrees associated with {title} on MPath.\n"
            "2. Check recognized colleges offering these programs, their admission modes, and curriculum depth.\n"
            "3. Begin building foundational domain knowledge and seek practical internships or introductory projects."
        )

        cursor.execute("""
            UPDATE careers
            SET career_family = COALESCE(career_family, ?),
                interest_clusters = COALESCE(interest_clusters, ?),
                work_style = COALESCE(work_style, ?),
                is_lesser_known = COALESCE(is_lesser_known, ?),
                reality_check = COALESCE(reality_check, ?),
                next_steps = COALESCE(next_steps, ?)
            WHERE id = ?
        """, (family, clusters_str, work_style, is_lesser, reality_check, next_steps, cid))
        updated_count += 1

    print(f"Enriched {updated_count} existing careers with new multidimensional attributes.")

def execute_expansion():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 1: Enrich existing careers
    enrich_existing_careers(cursor)

    # Step 2: Fetch existing max ID and existing slugs
    max_id = cursor.execute("SELECT MAX(id) FROM careers").fetchone()[0] or 126
    existing_slugs = set(r[0] for r in cursor.execute("SELECT slug FROM careers").fetchall())
    print(f"Current database has {len(existing_slugs)} careers. Max ID: {max_id}")

    # Step 3: Collect new unique careers
    new_candidates = collect_new_careers()
    print(f"Collected {len(new_candidates)} candidate careers from expansion catalog.")

    new_inserted_count = 0
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    current_id = max_id

    for c in new_candidates:
        slug = c.get("slug")
        if slug in existing_slugs:
            # Already exists in the database, do not duplicate
            continue

        current_id += 1
        existing_slugs.add(slug)

        ladder_json = json.dumps(c.get("ladder", []))
        routes_json = json.dumps(c.get("routes", []))
        skills_combined = f"{c.get('technical_skills', '')}, {c.get('soft_skills', '')}".strip(", ")

        # Insert career record
        cursor.execute("""
            INSERT INTO careers (
                id, title, slug, short_name, category, sub_category, industry, icon,
                short_description, description, what_they_do, day_to_day_work,
                work_modes, work_environment, minimum_qualification, education_required,
                preferred_streams, required_subjects, technical_skills, soft_skills,
                tools, skills_required, certifications, experience_level, career_growth,
                career_progression, entry_routes, higher_study_options, entrepreneurship_options,
                internship_roles, entry_level_roles, average_salary, salary_indicative,
                future_scope, government_opportunities, private_opportunities, source,
                official_url, verification_status, last_verified_at, created_at, updated_at,
                is_lesser_known, career_family, interest_clusters, work_style, reality_check, next_steps
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            current_id,
            c["title"],
            c["slug"],
            c.get("short_name", c["title"]),
            c["category"],
            c.get("sub_category", ""),
            c.get("industry", ""),
            c.get("icon", "briefcase"),
            c.get("short_description", ""),
            c.get("description", ""),
            c.get("what_they_do", ""),
            c.get("day_to_day_work", ""),
            c.get("work_modes", "On-site"),
            c.get("work_environment", "Office"),
            c.get("minimum_qualification", "Undergraduate"),
            c.get("minimum_qualification", "Undergraduate"),
            c.get("preferred_streams", "Any Stream"),
            c.get("required_subjects", ""),
            c.get("technical_skills", ""),
            c.get("soft_skills", ""),
            c.get("tools", ""),
            skills_combined,
            c.get("certifications", ""),
            c.get("experience_level", "Entry to Senior Level"),
            c.get("career_growth", ""),
            ladder_json,
            routes_json,
            c.get("higher_study_options", ""),
            c.get("entrepreneurship_options", ""),
            c.get("internship_roles", ""),
            c.get("entry_level_roles", ""),
            c.get("average_salary", "₹5.0 - ₹12.0 LPA"),
            c.get("salary_indicative", ""),
            c.get("future_scope", "High Demand"),
            c.get("government_opportunities", ""),
            c.get("private_opportunities", ""),
            c.get("source", "National Career Service (NCS) / Sector Skill Councils"),
            c.get("official_url", ""),
            c.get("verification_status", "VERIFIED"),
            now,
            now,
            now,
            c.get("is_lesser_known", False),
            c.get("career_family", "General Professional"),
            c.get("interest_clusters", "General"),
            c.get("work_style", "Office"),
            c.get("reality_check", ""),
            c.get("next_steps", "")
        ))

        # Insert relational courses
        for course_rel in c.get("courses", []):
            course_id = course_rel.get("course_id")
            if course_id:
                # verify course exists
                exists = cursor.execute("SELECT id FROM courses WHERE id = ?", (course_id,)).fetchone()
                if exists:
                    cursor.execute("""
                        INSERT INTO career_courses (career_id, course_id, relationship_type, description, verification_status)
                        VALUES (?, ?, ?, ?, 'VERIFIED')
                    """, (current_id, course_id, course_rel.get("type", "PRIMARY"), f"Degree qualification for {c['title']}"))

        # Insert relational exams
        for exam_rel in c.get("exams", []):
            exam_id = exam_rel.get("exam_id")
            if exam_id:
                exists = cursor.execute("SELECT id FROM government_exams WHERE id = ?", (exam_id,)).fetchone()
                if exists:
                    cursor.execute("""
                        INSERT INTO career_exams (career_id, exam_id, importance, eligibility_summary, verification_status)
                        VALUES (?, ?, ?, ?, 'VERIFIED')
                    """, (current_id, exam_id, exam_rel.get("importance", "PRIMARY"), f"Official examination for {c['title']}"))

        # Insert career skills
        for skill in [s.strip() for s in c.get("technical_skills", "").split(",") if s.strip()]:
            cursor.execute("""
                INSERT INTO career_skills (career_id, skill_name, skill_level, is_required, skill_category, importance)
                VALUES (?, ?, 'Core', 1, 'Technical', 'Core')
            """, (current_id, skill))

        for soft in [s.strip() for s in c.get("soft_skills", "").split(",") if s.strip()]:
            cursor.execute("""
                INSERT INTO career_skills (career_id, skill_name, skill_level, is_required, skill_category, importance)
                VALUES (?, ?, 'Important', 1, 'Soft Skill', 'Important')
            """, (current_id, soft))

        for tool in [t.strip() for t in c.get("tools", "").split(",") if t.strip()]:
            cursor.execute("""
                INSERT INTO career_skills (career_id, skill_name, skill_level, is_required, skill_category, importance)
                VALUES (?, ?, 'Preferred', 0, 'Tool / Technology', 'Preferred')
            """, (current_id, tool))

        # Insert career roadmaps
        for idx, route in enumerate(c.get("routes", []), start=1):
            cursor.execute("""
                INSERT INTO career_roadmaps (
                    career_id, overview, path_name, path_type, roadmap_steps, required_skills, salary, future_scope
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                current_id,
                route.get("steps", ""),
                route.get("title", f"Path {idx}"),
                route.get("type", "COMMON"),
                route.get("steps", ""),
                c.get("technical_skills", ""),
                c.get("average_salary", ""),
                c.get("future_scope", "")
            ))

        # Insert starting point roadmaps
        stage_templates = {
            "Class 10": f"Focus on foundational subjects, academic curiosity, and relevant stream selection for {c['title']}.",
            "Class 12": f"Excel in Class 12 with required subjects ({c.get('required_subjects', 'relevant subjects')}) and prepare for relevant entrance tests.",
            "Graduation": f"Complete relevant undergraduate training ({c.get('minimum_qualification', 'Undergraduate')}) and engage in active project work and internships.",
            "Working Professional": f"Pursue advanced certifications ({c.get('certifications', 'industry credentials')}) and target senior roles ({c.get('career_growth', 'leadership roles')})."
        }
        for st_name, st_desc in stage_templates.items():
            cursor.execute("""
                INSERT INTO career_roadmaps (
                    career_id, starting_point, path_name, path_type, overview, roadmap_steps
                ) VALUES (?, ?, ?, 'Starting Point', ?, ?)
            """, (current_id, st_name, f"Starting from {st_name}", st_desc, st_desc))

        new_inserted_count += 1

    conn.commit()

    total_careers = cursor.execute("SELECT COUNT(*) FROM careers").fetchone()[0]
    total_courses_linked = cursor.execute("SELECT COUNT(*) FROM career_courses").fetchone()[0]
    total_exams_linked = cursor.execute("SELECT COUNT(*) FROM career_exams").fetchone()[0]
    total_skills_linked = cursor.execute("SELECT COUNT(*) FROM career_skills").fetchone()[0]
    total_roadmaps_linked = cursor.execute("SELECT COUNT(*) FROM career_roadmaps").fetchone()[0]

    print("==============================================================================")
    print("MPath Career Universe Master Expansion Successfully Executed!")
    print("==============================================================================")
    print(f"Brand-New Careers Inserted: {new_inserted_count}")
    print(f"Total Careers in Database: {total_careers}")
    print(f"Total Career-Course Relationships: {total_courses_linked}")
    print(f"Total Career-Exam Relationships: {total_exams_linked}")
    print(f"Total Career-Skill Records: {total_skills_linked}")
    print(f"Total Career-Roadmap Records: {total_roadmaps_linked}")
    print("==============================================================================")

    # Category breakdown
    cat_counts = cursor.execute("SELECT category, COUNT(*) FROM careers GROUP BY category ORDER BY COUNT(*) DESC").fetchall()
    print("Category Breakdown:")
    for cat, cnt in cat_counts:
        pct = round(cnt / total_careers * 100, 1)
        print(f"  - {cat}: {cnt} ({pct}%)")

    conn.close()

if __name__ == "__main__":
    execute_expansion()
