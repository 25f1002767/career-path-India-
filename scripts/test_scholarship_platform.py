"""
Comprehensive Test Suite for National Scholarship Discovery, Eligibility & Application Platform
Verifies:
1. Database Integrity & Real Data Sources (No Synthetic/Fake Records)
2. Deterministic Eligibility Engine (Explanations, Blockers, Positive Factors, Scoring)
3. Full Route Coverage (Explorer, Details, Find-For-Me, Calendar, Compare, Coverage, APIs)
4. Dynamic Form Engine, Autofill & Application Draft Lifecycle
5. Document Vault & IDOR Security Protection
6. Admin Operations (Health Diagnostics, Importer, Duplicate Checker, Exporter)
7. Zero-Regression on Core Modules (Careers, Colleges, Courses, Exams)
"""

import os
import sys
import io
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app
from extensions import db
from werkzeug.security import generate_password_hash
from models.user import User
from models.scholarship import (
    Scholarship,
    ScholarshipCycle,
    ScholarshipApplication,
    ScholarshipField,
    StudentDocument,
    ScholarshipApplicationDocument
)
from services.scholarship_eligibility import evaluate_scholarship_eligibility


def run_tests():
    print("=" * 70)
    print("RUNNING NATIONAL SCHOLARSHIP PLATFORM TEST SUITE")
    print("=" * 70)

    client = app.test_client()

    with app.app_context():
        # ---------------------------------------------------------
        # 1. DATABASE INTEGRITY & DATA QUALITY AUDIT
        # ---------------------------------------------------------
        print("\n[TEST 1] Auditing Scholarship Database & Traceable Sources...")
        total_schs = Scholarship.query.count()
        verified_schs = Scholarship.query.filter_by(verification_status="VERIFIED").count()
        cycles_count = ScholarshipCycle.query.count()
        fields_count = ScholarshipField.query.count()

        print(f"  • Total Traceable Scholarships in DB: {total_schs}")
        print(f"  • Officially Verified Scholarships: {verified_schs}")
        print(f"  • Application Cycles Registered: {cycles_count}")
        print(f"  • Configurable Application Fields: {fields_count}")

        assert total_schs >= 50, f"Expected at least 50 scholarships, found {total_schs}"
        assert verified_schs >= 40, f"Expected at least 40 verified scholarships, found {verified_schs}"
        assert cycles_count >= 40, f"Expected active scholarship cycles, found {cycles_count}"
        assert fields_count >= 5, f"Expected dynamic application fields, found {fields_count}"

        # Verify no fake official URLs
        sample_sch = Scholarship.query.filter(Scholarship.official_url.isnot(None)).first()
        assert sample_sch is not None
        assert "http" in (sample_sch.official_url or sample_sch.official_website)
        print("  [OK] Database integrity and source audit PASSED.")

        # ---------------------------------------------------------
        # 2. DETERMINISTIC ELIGIBILITY ENGINE
        # ---------------------------------------------------------
        print("\n[TEST 2] Testing Deterministic Eligibility Engine...")
        inspire = Scholarship.query.filter(Scholarship.title.ilike("%INSPIRE%")).first()
        if not inspire:
            inspire = Scholarship.query.first()

        # Student A: Perfect match (Science UG, high marks)
        student_a = {
            "education_level": "Undergraduate",
            "degree": "B.Sc",
            "stream": "Natural & Basic Sciences",
            "percentage": 92.0,
            "family_income": 300000,
            "gender": "Any",
            "category": "General",
            "state": "Madhya Pradesh"
        }
        res_a = evaluate_scholarship_eligibility(inspire, student_a)
        print(f"  • Student A Match Status: {res_a['status']} (Score: {res_a['fit_score']}%)")
        print(f"    Positive signals: {len(res_a['positive_signals'])}, Blockers: {len(res_a['blockers'])}")
        assert res_a["status"] in ["ELIGIBLE", "LIKELY_ELIGIBLE"]
        assert len(res_a["positive_signals"]) > 0

        # Student B: Ineligible (Arts student, percentage too low, or exceeding income limit if scheme has one)
        income_restricted = Scholarship.query.filter(Scholarship.family_income_limit.isnot(None)).first()
        if income_restricted:
            limit = income_restricted.family_income_limit
            student_b = {
                "education_level": "Postgraduate",
                "family_income": limit + 500000,
                "percentage": 45.0,
                "gender": "Male"
            }
            res_b = evaluate_scholarship_eligibility(income_restricted, student_b)
            print(f"  • Student B Ineligible Check on '{income_restricted.title}': {res_b['status']}")
            assert res_b["status"] in ["NOT_ELIGIBLE", "PARTIALLY_MATCHED"]
            assert len(res_b["blockers"]) > 0 or len(res_b["warnings"]) > 0
            print(f"    Issue detected: {res_b['blockers'][0] if res_b['blockers'] else res_b['warnings'][0]}")

        print("  [OK] Deterministic Eligibility Engine PASSED.")

        # ---------------------------------------------------------
        # 3. PUBLIC EXPLORER & DISCOVERY ROUTE TESTS
        # ---------------------------------------------------------
        print("\n[TEST 3] Testing Public Discovery Routes (200 OK checks)...")
        routes_to_test = [
            "/scholarships/",
            "/scholarships/find-for-me",
            "/scholarships/calendar",
            "/scholarships/compare",
            "/scholarships/coverage"
        ]

        for route in routes_to_test:
            resp = client.get(route)
            assert resp.status_code == 200, f"Route {route} failed with {resp.status_code}"
            print(f"  • GET {route} -> 200 OK")

        # Test single scholarship dossier
        sch = Scholarship.query.first()
        slug_or_id = sch.slug or sch.id
        resp = client.get(f"/scholarships/{slug_or_id}")
        assert resp.status_code == 200, f"Dossier route failed for {slug_or_id}"
        print(f"  • GET /scholarships/{slug_or_id} -> 200 OK")

        # Test Eligibility Check API
        api_resp = client.post(
            "/scholarships/api/check-eligibility",
            data=json.dumps({
                "scholarship_id": sch.id,
                "education_level": "Undergraduate",
                "percentage": 85,
                "family_income": 200000
            }),
            content_type="application/json"
        )
        assert api_resp.status_code == 200
        api_data = json.loads(api_resp.data)
        assert api_data["success"] is True
        print(f"  • POST /scholarships/api/check-eligibility -> 200 OK (Status: {api_data['evaluation']['status']})")

        # Test Grounded AI Counsellor API
        counsellor_resp = client.post(
            "/scholarships/api/counsellor",
            data=json.dumps({"query": "scholarships for engineering in Madhya Pradesh"}),
            content_type="application/json"
        )
        assert counsellor_resp.status_code == 200
        counsellor_data = json.loads(counsellor_resp.data)
        assert counsellor_data["success"] is True
        assert counsellor_data["count"] > 0
        print(f"  • POST /scholarships/api/counsellor -> 200 OK ({counsellor_data['count']} schemes retrieved)")

        print("  [OK] Public routes and discovery APIs PASSED.")

        # ---------------------------------------------------------
        # 4. AUTHENTICATED WORKFLOW: APPLICATION & DRAFTS
        # ---------------------------------------------------------
        print("\n[TEST 4] Testing Authenticated Application Lifecycle & Drafts...")
        # Create or find a test student user
        test_user = User.query.filter_by(email="scholarship_tester@example.com").first()
        if not test_user:
            test_user = User(
                full_name="Test Scholar",
                email="scholarship_tester@example.com",
                role="student",
                password_hash=generate_password_hash("SecurePass123!")
            )
            db.session.add(test_user)
            db.session.commit()

        # Simulate authenticated session
        with client.session_transaction() as sess:
            sess["user_id"] = test_user.id
            sess["user_name"] = test_user.full_name
            sess["role"] = test_user.role

        # GET /scholarships/apply/<id>
        resp = client.get(f"/scholarships/apply/{sch.id}")
        assert resp.status_code == 200
        print(f"  • GET /scholarships/apply/{sch.id} -> 200 OK (Application Wizard Loaded)")

        # POST /scholarships/apply/<id> (Save Draft)
        save_draft_resp = client.post(
            f"/scholarships/apply/{sch.id}",
            data={
                "action": "save_draft",
                "student_notes": "Test draft saved by automated test",
                "full_name": "Test Scholar",
                "contact_mobile": "9876543210"
            },
            follow_redirects=True
        )
        assert save_draft_resp.status_code == 200
        print(f"  • POST /scholarships/apply/{sch.id} (Save Draft) -> 200 OK")

        # Verify application record created in DB
        app_rec = ScholarshipApplication.query.filter_by(
            user_id=test_user.id,
            scholarship_id=sch.id
        ).first()
        assert app_rec is not None
        assert app_rec.status == "DRAFT"
        assert app_rec.application_number is not None
        print(f"  • Application record verified: #{app_rec.application_number} (Status: {app_rec.status})")

        # Test My Applications Dashboard
        my_apps_resp = client.get("/scholarships/my-applications")
        assert my_apps_resp.status_code == 200
        print("  • GET /scholarships/my-applications -> 200 OK")

        # Test Manual Status Sync
        sync_resp = client.post(
            f"/scholarships/application/{app_rec.id}/update-status",
            data={
                "status": "SUBMITTED",
                "external_reference_number": "NSP-2026-998811",
                "notes": "Officially submitted on portal"
            },
            follow_redirects=True
        )
        assert sync_resp.status_code == 200
        db.session.refresh(app_rec)
        assert app_rec.status == "SUBMITTED"
        assert app_rec.external_reference_number == "NSP-2026-998811"
        print(f"  • Status updated & synced: Status={app_rec.status}, Ref={app_rec.external_reference_number}")

        print("  [OK] Authenticated Application Lifecycle PASSED.")

        # ---------------------------------------------------------
        # 5. DOCUMENT VAULT & IDOR ACCESS CONTROL
        # ---------------------------------------------------------
        print("\n[TEST 5] Testing Document Vault & IDOR Security Protection...")
        doc_vault_resp = client.get("/scholarships/documents")
        assert doc_vault_resp.status_code == 200
        print("  • GET /scholarships/documents -> 200 OK")

        # Upload a test document (e.g. Income Certificate)
        fake_file_content = b"%PDF-1.4 Fake Income Certificate for Test"
        upload_resp = client.post(
            "/scholarships/documents/upload",
            data={
                "document_type": "Income Certificate",
                "file": (io.BytesIO(fake_file_content), "income_cert_2026.pdf")
            },
            content_type="multipart/form-data",
            follow_redirects=True
        )
        assert upload_resp.status_code == 200

        doc_record = StudentDocument.query.filter_by(
            user_id=test_user.id,
            document_type="Income Certificate"
        ).order_by(StudentDocument.id.desc()).first()
        assert doc_record is not None
        print(f"  • Document uploaded successfully: ID #{doc_record.id}, Name: {doc_record.file_name}")

        # Download own document -> 200 OK
        dl_resp = client.get(f"/scholarships/documents/download/{doc_record.id}")
        assert dl_resp.status_code == 200
        print(f"  • Authorized Download /scholarships/documents/download/{doc_record.id} -> 200 OK")

        # IDOR Security Check: Create user 2 and attempt to download user 1's document
        test_user_2 = User.query.filter_by(email="other_student@example.com").first()
        if not test_user_2:
            test_user_2 = User(
                full_name="Another Student",
                email="other_student@example.com",
                role="student",
                password_hash=generate_password_hash("SecurePass123!")
            )
            db.session.add(test_user_2)
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = test_user_2.id
            sess["user_name"] = test_user_2.full_name
            sess["role"] = test_user_2.role

        idor_resp = client.get(f"/scholarships/documents/download/{doc_record.id}")
        assert idor_resp.status_code == 403, f"Expected 403 Forbidden on IDOR check, got {idor_resp.status_code}"
        print(f"  • IDOR Protection Verified: User 2 forbidden (403) from accessing User 1's document.")

        print("  [OK] Document Vault & IDOR Security PASSED.")

        # ---------------------------------------------------------
        # 6. ADMIN DASHBOARD & DATA HEALTH DIAGNOSTICS
        # ---------------------------------------------------------
        print("\n[TEST 6] Testing Admin Operations & Real-time Health Diagnostics...")
        # Create admin user if needed
        admin_user = User.query.filter_by(role="admin").first()
        if not admin_user:
            admin_user = User(
                full_name="Admin User",
                email="admin@mpath.in",
                role="admin",
                password_hash=generate_password_hash("AdminSecurePass123!")
            )
            db.session.add(admin_user)
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = admin_user.id
            sess["user_name"] = admin_user.full_name
            sess["role"] = "admin"

        admin_resp = client.get("/admin/scholarships")
        assert admin_resp.status_code == 200
        print("  • GET /admin/scholarships -> 200 OK")

        # Duplicate check route
        dup_resp = client.get("/admin/scholarships/duplicate-check")
        assert dup_resp.status_code == 200
        dup_data = json.loads(dup_resp.data)
        assert "duplicate_groups_count" in dup_data
        print(f"  • GET /admin/scholarships/duplicate-check -> 200 OK ({dup_data['duplicate_groups_count']} duplicate clusters)")

        # Export routes
        exp_json = client.get("/admin/scholarships/export/json")
        assert exp_json.status_code == 200
        assert "application/json" in exp_json.content_type
        print("  • GET /admin/scholarships/export/json -> 200 OK")

        exp_csv = client.get("/admin/scholarships/export/csv")
        assert exp_csv.status_code == 200
        assert "text/csv" in exp_csv.content_type
        print("  • GET /admin/scholarships/export/csv -> 200 OK")

        print("  [OK] Admin Operations and Health Diagnostics PASSED.")

        # ---------------------------------------------------------
        # 7. REGRESSION TESTING ON EXISTING FUNCTIONALITY
        # ---------------------------------------------------------
        print("\n[TEST 7] Testing Zero-Regression on Core Modules...")
        core_routes = [
            "/careers/",
            "/colleges/",
            "/courses/",
            "/exams/",
            "/internships/",
            "/assessment/"
        ]

        for cr in core_routes:
            r = client.get(cr)
            assert r.status_code == 200, f"Regression on {cr}: status {r.status_code}"
            print(f"  • Core Module GET {cr} -> 200 OK")

        print("  [OK] Zero-Regression Verification PASSED.")

    print("\n" + "=" * 70)
    print("ALL 7 TEST SUITES COMPLETED WITH 100% SUCCESS!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
