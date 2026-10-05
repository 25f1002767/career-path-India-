"""
scripts/execute_master_career_seed.py
==============================================================================
National Career Discovery Platform - Master Seeding Pipeline (126 Careers)
==============================================================================
Seeds 126 authentic occupational pathways across 14 official sectors.
Populates:
  - careers (core metadata, descriptions, salaries, sources)
  - career_courses (relational links to canonical courses)
  - career_exams (relational links to canonical exams)
  - career_skills (technical, soft, and tool taxonomy)
  - career_roadmaps (multi-route pathways and starting-point roadmaps)
==============================================================================
"""

import sqlite3
import json
import inspect
from datetime import datetime

DB_PATH = "careerpathindia.db"

def collect_all_careers():
    careers = []
    
    from scripts.career_dataset import CAREERS_DATA as TECH_PART1
    from scripts.seed_comprehensive_careers import ADDITIONAL_CAREERS as TECH_AND_HEALTH
    from scripts.careers_data_extended import FINANCE_CAREERS
    from scripts.careers_data_part2 import ENGINEERING_CAREERS
    from scripts.careers_data_part3 import REMAINING_CAREERS

    careers.extend(TECH_PART1)
    careers.extend(TECH_AND_HEALTH)
    careers.extend(FINANCE_CAREERS)
    careers.extend(ENGINEERING_CAREERS)
    careers.extend(REMAINING_CAREERS)

    for i in range(1, 13):
        mod_name = f"scripts.catalog_builder_part{i}" if i > 1 else "scripts.catalog_builder"
        m = __import__(mod_name, fromlist=["dummy"])
        funcs = [getattr(m, k) for k, v in inspect.getmembers(m, inspect.isfunction) if k.startswith("get_")]
        for fn in funcs:
            careers.extend(fn())

    seen = set()
    unique = []
    for c in careers:
        if c["slug"] not in seen:
            seen.add(c["slug"])
            unique.append(c)

    print(f"Total authentic careers collected: {len(unique)}")
    return unique

def seed_database():
    careers = collect_all_careers()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Clean existing career relations to prevent foreign key orphan states
    cursor.execute("DELETE FROM career_courses")
    cursor.execute("DELETE FROM career_exams")
    cursor.execute("DELETE FROM career_skills")
    cursor.execute("DELETE FROM career_roadmaps")
    cursor.execute("DELETE FROM careers")
    conn.commit()

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    inserted_career_count = 0
    total_courses_linked = 0
    total_exams_linked = 0
    total_skills_linked = 0
    total_roadmaps_linked = 0

    for idx, c in enumerate(careers, start=1):
        # Insert career
        ladder_json = json.dumps(c.get("ladder", []))
        routes_json = json.dumps(c.get("routes", []))
        skills_combined = f"{c.get('technical_skills', '')}, {c.get('soft_skills', '')}".strip(", ")

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
                official_url, verification_status, last_verified_at, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            idx,
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
            c.get("work_modes", "Hybrid / Office"),
            c.get("work_environment", ""),
            c.get("minimum_qualification", "Undergraduate Degree"),
            c.get("minimum_qualification", "Undergraduate Degree"),
            c.get("preferred_streams", ""),
            c.get("required_subjects", ""),
            c.get("technical_skills", ""),
            c.get("soft_skills", ""),
            c.get("tools", ""),
            skills_combined,
            c.get("certifications", ""),
            c.get("experience_level", "Entry-Level to Senior"),
            c.get("career_growth", ""),
            ladder_json,
            routes_json,
            c.get("higher_study_options", ""),
            c.get("entrepreneurship_options", ""),
            c.get("internship_roles", ""),
            c.get("entry_level_roles", ""),
            c.get("average_salary", "₹4 - ₹12 LPA"),
            c.get("salary_indicative", ""),
            c.get("future_scope", ""),
            c.get("government_opportunities", ""),
            c.get("private_opportunities", ""),
            c.get("source", "National Career Service (NCS) / Sector Skill Councils"),
            c.get("official_url", "https://www.ncs.gov.in"),
            c.get("verification_status", "VERIFIED"),
            now,
            now,
            now
        ))
        inserted_career_count += 1

        # 2. Link courses
        for course_spec in c.get("courses", []):
            course_id = course_spec.get("course_id")
            rel_type = course_spec.get("type", "COMMON")
            cursor.execute("""
                INSERT INTO career_courses (
                    career_id, course_id, relationship_type, description, verification_status
                ) VALUES (?, ?, ?, ?, ?)
            """, (idx, course_id, rel_type, f"{rel_type} pathway course", "VERIFIED"))
            total_courses_linked += 1

        # 3. Link exams
        for exam_spec in c.get("exams", []):
            exam_id = exam_spec.get("exam_id")
            importance = exam_spec.get("importance", "PRIMARY")
            cursor.execute("""
                INSERT INTO career_exams (
                    career_id, exam_id, importance, eligibility_summary, verification_status
                ) VALUES (?, ?, ?, ?, ?)
            """, (idx, exam_id, importance, f"{importance} entrance / recruitment examination", "VERIFIED"))
            total_exams_linked += 1

        # 4. Link skills (Technical, Soft, Tools)
        tech_skills = [s.strip() for s in c.get("technical_skills", "").split(",") if s.strip()]
        for s in tech_skills:
            cursor.execute("""
                INSERT INTO career_skills (
                    career_id, skill_name, skill_level, is_required, skill_category, importance
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (idx, s, "Intermediate", 1, "Technical", "Core"))
            total_skills_linked += 1

        soft_skills = [s.strip() for s in c.get("soft_skills", "").split(",") if s.strip()]
        for s in soft_skills:
            cursor.execute("""
                INSERT INTO career_skills (
                    career_id, skill_name, skill_level, is_required, skill_category, importance
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (idx, s, "General", 1, "Soft Skill", "Important"))
            total_skills_linked += 1

        tools = [s.strip() for s in c.get("tools", "").split(",") if s.strip()]
        for s in tools:
            cursor.execute("""
                INSERT INTO career_skills (
                    career_id, skill_name, skill_level, is_required, skill_category, importance
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (idx, s, "Proficient", 0, "Tool / Technology", "Preferred"))
            total_skills_linked += 1

        # 5. Link roadmaps
        # Routes
        for r in c.get("routes", []):
            cursor.execute("""
                INSERT INTO career_roadmaps (
                    career_id, path_name, path_type, roadmap_steps, overview, salary, future_scope
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                idx,
                r.get("title", "Alternative Pathway"),
                r.get("type", "COMMON"),
                r.get("steps", ""),
                c.get("description", ""),
                c.get("average_salary", ""),
                c.get("future_scope", "")
            ))
            total_roadmaps_linked += 1

        # Starting points
        for sp, step_text in c.get("roadmaps", {}).items():
            cursor.execute("""
                INSERT INTO career_roadmaps (
                    career_id, starting_point, path_type, roadmap_steps, overview
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                idx,
                sp,
                "Starting Point",
                step_text,
                f"Guidance starting from {sp}"
            ))
            total_roadmaps_linked += 1

    conn.commit()
    conn.close()

    print("==============================================================================")
    print("MASTER SEEDING COMPLETED SUCCESSFULLY!")
    print(f"Careers inserted: {inserted_career_count}")
    print(f"Course linkages created: {total_courses_linked}")
    print(f"Exam linkages created: {total_exams_linked}")
    print(f"Structured skills indexed: {total_skills_linked}")
    print(f"Multi-route and starting-point roadmaps created: {total_roadmaps_linked}")
    print("==============================================================================")

if __name__ == "__main__":
    seed_database()
