"""
scripts/test_career_counselling_system.py
==============================================================================
National Career Discovery Platform - Verification & Test Suite
==============================================================================
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models.career import Career
from models.career_course import CareerCourse
from models.career_exam import CareerExam
from models.career_skill import CareerSkill
from models.roadmap import CareerRoadmap
from models.course import Course, CollegeCourse
from models.college import College
from models.exam import GovernmentExam

def run_tests():
    print("==============================================================================")
    print("RUNNING NATIONAL CAREER DISCOVERY & COUNSELLING TEST SUITE")
    print("==============================================================================")

    with app.app_context():
        # 1. Database Quantitative Audits
        careers_count = Career.query.count()
        print(f"[TEST 1] Career count: {careers_count}")
        assert careers_count >= 126, f"Expected at least 126 careers, got {careers_count}"

        slugs = [c.slug for c in Career.query.all()]
        assert len(slugs) == len(set(slugs)), "Career slugs must be unique!"
        print(f"[TEST 2] Slugs uniqueness: PASSED ({len(slugs)} unique slugs)")

        sectors = {c.category for c in Career.query.all()}
        print(f"[TEST 3] Sectors represented: {len(sectors)} (>= 14 required)")
        assert len(sectors) >= 14, f"Expected at least 14 sectors, got {len(sectors)}"

        course_links = CareerCourse.query.count()
        print(f"[TEST 4] Career -> Course linkages: {course_links}")
        assert course_links >= 300, f"Expected >= 300 course linkages, got {course_links}"

        exam_links = CareerExam.query.count()
        print(f"[TEST 5] Career -> Exam linkages: {exam_links}")
        assert exam_links >= 200, f"Expected >= 200 exam linkages, got {exam_links}"

        skills_count = CareerSkill.query.count()
        print(f"[TEST 6] Indexed skills count: {skills_count}")
        assert skills_count >= 1500, f"Expected >= 1500 skills, got {skills_count}"

        roadmaps_count = CareerRoadmap.query.count()
        print(f"[TEST 7] Multi-route & starting-point roadmaps: {roadmaps_count}")
        assert roadmaps_count >= 600, f"Expected >= 600 roadmaps, got {roadmaps_count}"

        # 2. Graph Traversal Test: Career -> Course -> CollegeCourse -> College
        sample_career = Career.query.filter_by(slug="data-scientist").first()
        assert sample_career is not None, "Data Scientist career must exist"
        linked_courses = CareerCourse.query.filter_by(career_id=sample_career.id).all()
        assert len(linked_courses) > 0, "Data Scientist must have linked courses"
        first_course_id = linked_courses[0].course_id
        offering_colleges = (
            College.query.join(CollegeCourse, College.id == CollegeCourse.college_id)
            .filter(CollegeCourse.course_id == first_course_id)
            .limit(5)
            .all()
        )
        print(f"[TEST 8] Relational graph traversal (Career -> Course -> Colleges): PASSED ({len(offering_colleges)} colleges discovered for course ID {first_course_id})")

    # 3. HTTP Endpoints Testing via Test Client
    client = app.test_client()

    # Route 1: Career List
    res = client.get("/careers/")
    assert res.status_code == 200, f"/careers/ failed with status {res.status_code}"
    assert b"National Career Discovery" in res.data, "Career list page must contain hero header"
    print("[TEST 9] GET /careers/ -> 200 OK")

    # Route 2: Category Filter
    res = client.get("/careers/?category=Technology+%26+Computer+Science")
    assert res.status_code == 200
    print("[TEST 10] GET /careers/?category=... -> 200 OK")

    # Route 3: Category Landing Page
    res = client.get("/careers/category/technology-computer-science")
    assert (b"Technology & Computer Science" in res.data or b"Technology &amp; Computer Science" in res.data)
    print("[TEST 11] GET /careers/category/technology-computer-science -> 200 OK")

    # Route 4: Career Dossier Details Page
    res = client.get("/careers/data-scientist")
    assert res.status_code == 200
    assert b"Data Scientist" in res.data
    assert b"Career Fit Explorer" in res.data
    assert b"AI Career Counsellor" in res.data
    print("[TEST 12] GET /careers/data-scientist (Dossier) -> 200 OK")

    # Route 5: Discover Questionnaire (GET)
    res = client.get("/careers/discover")
    assert res.status_code == 200
    assert b"Help Me Discover Careers" in res.data
    print("[TEST 13] GET /careers/discover -> 200 OK")

    # Route 6: Discover Questionnaire (POST)
    res = client.post("/careers/discover", data={
        "current_status": "Class 12",
        "stream": "Science (PCM)",
        "math_affinity": "5",
        "tech_affinity": "5",
        "creative_affinity": "3",
        "people_affinity": "2",
        "work_mode_pref": "Hybrid",
        "preferred_orientation": "High Tech & Innovation"
    })
    assert res.status_code == 200
    assert b"Your Personalized Discovery Results" in res.data
    print("[TEST 14] POST /careers/discover -> 200 OK")

    # Route 7: Explore by Course
    res = client.get("/careers/explore-by-course?course_id=1")
    assert res.status_code == 200
    print("[TEST 15] GET /careers/explore-by-course?course_id=1 -> 200 OK")

    # Route 8: Explore by Skills
    res = client.get("/careers/explore-by-skills?skill=Python")
    assert res.status_code == 200
    assert b"Careers Requiring:" in res.data
    print("[TEST 16] GET /careers/explore-by-skills?skill=Python -> 200 OK")

    # Route 9: Explore by Subject
    res = client.get("/careers/explore-by-subject?subject=Mathematics")
    assert res.status_code == 200
    assert b"Careers Relying on" in res.data
    print("[TEST 17] GET /careers/explore-by-subject?subject=Mathematics -> 200 OK")

    # Route 10: Career Comparison
    res = client.get("/careers/compare?career1=data-scientist&career2=ai-engineer")
    assert res.status_code == 200
    assert b"Side-by-Side Comparison" in res.data
    print("[TEST 18] GET /careers/compare -> 200 OK")

    # Route 11: Interactive Fit Calculator API
    res = client.post("/careers/api/fit-calculator", json={
        "career_id": 1,
        "stream": "Science (PCM)",
        "work_mode_pref": "Hybrid",
        "math_affinity": 4,
        "tech_affinity": 5,
        "people_affinity": 3,
        "creative_affinity": 3
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "fit_score" in data
    assert "verdict" in data
    print(f"[TEST 19] POST /careers/api/fit-calculator -> 200 OK (Fit Score: {data['fit_score']}%)")

    # Route 12: Grounded AI Counsellor API
    res = client.post("/careers/api/counsellor", json={
        "query": "How can I become an AI Engineer?",
        "career_slug": "ai-engineer"
    })
    assert res.status_code == 200
    c_data = res.get_json()
    assert c_data.get("success") is True
    assert "MPath" in c_data.get("response", "")
    print("[TEST 20] POST /careers/api/counsellor -> 200 OK")

    print("==============================================================================")
    print("ALL 20 SYSTEM VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("==============================================================================")

if __name__ == "__main__":
    run_tests()
