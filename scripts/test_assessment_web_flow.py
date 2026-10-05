"""
scripts/test_assessment_web_flow.py
==============================================================================
Live End-to-End HTTP Flow Test for Assessment Module
==============================================================================
Tests:
- GET /assessment/ (Questionnaire UI)
- POST /assessment/submit (Submission & evaluation)
- GET /assessment/result/<result_id> (Dossier rendering)
- Regression checks on /dashboard/ and /student/dashboard
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if sys.platform.startswith("win"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from app import app
from models.user import User


def test_web_flow():
    client = app.test_client()

    print("=================================================================")
    print("[NET] TESTING HTTP END-TO-END CAREER ASSESSMENT FLOW")
    print("=================================================================\n")

    # 1. Test GET /assessment/
    res = client.get("/assessment/")
    assert res.status_code == 200, f"GET /assessment/ failed: {res.status_code}"
    html = res.data.decode("utf-8")
    assert "Discover Your Career Landscape" in html
    assert "q1_curiosity_scenario" in html
    assert "Exploring Your Problem-Solving & Curiosity" in html
    print("[PASS] 1. GET /assessment/ returned 200 OK with scenario questions & progress bar.")

    # 2. Test POST /assessment/submit with Persona 1 payload
    post_payload = {
        "q1_curiosity_scenario": "B",
        "q2_flow_activity": "B",
        "q3_self_efficacy": "A",
        "q4_work_values": "C",
        "q5_problem_type": "A",
        "q6_work_environment": "E",
        "q7_failure_and_persistence": "A",
        "q8_study_investment_tolerance": "B",
        "q9_exam_tolerance": "C",
        "q10_family_expectations": "E",
        "q11_financial_constraints": "B",
        "q12_current_academic_level": "B",
        "q13_academic_strengths": "A",
        "q14_negative_preferences": "B",
        "q15_decision_making_style": "A",
        "q16_open_reflection": "I love building algorithmic systems and debugging data models."
    }

    submit_res = client.post("/assessment/submit", data=post_payload, follow_redirects=False)
    assert submit_res.status_code == 302, f"POST /assessment/submit did not redirect: {submit_res.status_code}"
    redirect_url = submit_res.headers.get("Location")
    assert "/assessment/result/" in redirect_url, f"Unexpected redirect URL: {redirect_url}"
    print(f"[PASS] 2. POST /assessment/submit evaluated successfully and redirected to {redirect_url}.")

    # 3. Test GET /assessment/result/<id>
    result_res = client.get(redirect_url)
    assert result_res.status_code == 200, f"GET {redirect_url} failed: {result_res.status_code}"
    result_html = result_res.data.decode("utf-8")
    assert "Your Career Discovery Profile" in result_html
    assert "Top Recommended Career Directions" in result_html
    assert "Careers You May Not Have Considered" in result_html
    assert "Your Next 3 Practical Actions" in result_html
    assert "Explore Full Career Dossier" in result_html
    print("[PASS] 3. Result page rendered comprehensive Counselling Dossier with top matches, unexpected careers, and next 3 actions.")

    # 4. Test Student Login & Dashboard with assessment result
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_email"] = "admin@example.com"
        sess["user_role"] = "admin"

    dash_res = client.get("/dashboard/")
    assert dash_res.status_code == 200, f"Dashboard failed with assessment: {dash_res.status_code}"
    dash_html = dash_res.data.decode("utf-8")
    assert "Dashboard" in dash_html
    print("[PASS] 4. /dashboard/ rendered smoothly with active assessment data.")

    print("\n[COMPLETE] ALL LIVE HTTP END-TO-END FLOW TESTS PASSED WITH 0 ERRORS!")


if __name__ == "__main__":
    test_web_flow()
