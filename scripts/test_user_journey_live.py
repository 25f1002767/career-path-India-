"""
Comprehensive Live User Journey & End-to-End Verification
==========================================================
Directly tests Section 22's 10 User Journey tests against the running Flask app.
Verifies:
- Test 1: Scholarship list page loads (200 OK)
- Test 2: Scholarship detail page loads (200 OK)
- Test 3: Official Website button points to real provider homepage (e.g. https://www.education.gov.in)
- Test 4: Apply Now button routes to official application starting portal (e.g. NSP OTR instructions)
- Test 5: Scholarship with no application URL displays 'Application Link Unavailable'
- Test 6: Expired scholarship displays 'Application Closed'
- Test 7: External government portal transfer via controlled redirect (safe gateway)
- Test 8: Legitimate URL redirection
- Test 9: Invalid/malicious URL schemes (e.g. javascript:, data:, localhost) are rejected
- Test 10: Mobile responsiveness check (viewport metadata and clean rendering)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models.scholarship import Scholarship, ScholarshipCycle, is_valid_http_url


class TestUserJourneyEndToEnd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_journey_1_scholarship_list(self):
        """TEST 1: Open scholarship list"""
        resp = self.client.get("/scholarships/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"National Scholarship Directory & Discovery", resp.data)
        self.assertIn(b"Central Sector Scheme", resp.data)

    def test_journey_2_scholarship_detail(self):
        """TEST 2: Open scholarship detail page"""
        resp = self.client.get("/scholarships/1")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Central Sector Scheme", resp.data)
        self.assertIn(b"Department of Higher Education", resp.data)

    def test_journey_3_official_website_button(self):
        """TEST 3: Click Official Website -> Must point to provider homepage"""
        sch = db.session.get(Scholarship, 1)
        self.assertIsNotNone(sch)
        # Verify provider website is separate from application portal
        self.assertEqual(sch.resolved_official_website, "https://www.education.gov.in")
        self.assertNotEqual(sch.resolved_official_website, sch.resolved_application_url)

        # In template HTML, verify link exists
        resp = self.client.get(f"/scholarships/{sch.id}")
        self.assertIn(b"https://www.education.gov.in", resp.data)
        self.assertIn(b"Official Website", resp.data)

    def test_journey_4_click_apply_now(self):
        """TEST 4: Click Apply -> Reaches real application starting page, NOT root homepage"""
        sch = db.session.get(Scholarship, 1)
        # Expected application page is NSP 2026-27 Application Portal
        self.assertEqual(sch.resolved_application_url, "https://scholarships.gov.in/ApplicationForm/")
        
        # Test departure gateway
        resp = self.client.get(f"/scholarships/{sch.id}/apply-redirect")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"You are being redirected to the official application portal", resp.data)
        self.assertIn(b"https://scholarships.gov.in/ApplicationForm/", resp.data)

        # Confirm redirect transfers to the exact application page
        resp_confirm = self.client.get(f"/scholarships/{sch.id}/apply-redirect?confirm=1")
        self.assertEqual(resp_confirm.status_code, 302)
        self.assertEqual(resp_confirm.headers["Location"], "https://scholarships.gov.in/ApplicationForm/")

    def test_journey_5_no_application_url(self):
        """TEST 5: Test a scholarship with no application URL -> Shows 'Application Link Unavailable'"""
        temp = Scholarship(
            title="Scheme Without App Link",
            slug="scheme-without-app-link",
            provider="State Board",
            official_website="https://www.stateboard.gov.in",
            official_application_url=None,
            application_url_status="MISSING",
            verification_status="VERIFIED"
        )
        db.session.add(temp)
        db.session.commit()

        # Check detail page
        resp = self.client.get(f"/scholarships/{temp.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Application Link Unavailable", resp.data)
        # Official website must still be accessible
        self.assertIn(b"https://www.stateboard.gov.in", resp.data)

        # Check direct redirect attempt
        resp_red = self.client.get(f"/scholarships/{temp.id}/apply-redirect?confirm=1")
        self.assertEqual(resp_red.status_code, 200)
        self.assertIn(b"Application Link Unavailable", resp_red.data)

        db.session.delete(temp)
        db.session.commit()

    def test_journey_6_expired_scholarship(self):
        """TEST 6: Test expired scholarship -> Shows 'Application Closed'"""
        temp = Scholarship(
            title="Expired Test Scholarship",
            slug="expired-test-scholarship",
            provider="Ministry of Education",
            official_website="https://www.education.gov.in",
            official_application_url="https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
            application_url_status="VALID",
            verification_status="VERIFIED"
        )
        db.session.add(temp)
        db.session.commit()

        cycle = ScholarshipCycle(
            scholarship_id=temp.id,
            academic_year="2025-2026",
            status="CLOSED",
            application_end_date="2025-12-31"
        )
        db.session.add(cycle)
        db.session.commit()

        # Check detail page shows Application Closed
        resp = self.client.get(f"/scholarships/{temp.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Application Closed", resp.data)

        # Attempt to redirect is blocked
        resp_red = self.client.get(f"/scholarships/{temp.id}/apply-redirect?confirm=1")
        self.assertEqual(resp_red.status_code, 200)
        self.assertIn(b"The application window for this scholarship cycle is closed", resp_red.data)

        db.session.delete(cycle)
        db.session.delete(temp)
        db.session.commit()

    def test_journey_7_external_portal_safety(self):
        """TEST 7: Test external government application portal safety (no credential harvesting)"""
        resp = self.client.get("/scholarships/8/apply-redirect")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"External Application Portal Advisory", resp.data)
        # Ensure destination is the official DST INSPIRE application registration portal
        self.assertIn(b"https://online-inspire.gov.in/Account/Register", resp.data)

    def test_journey_8_redirect_handling(self):
        """TEST 8: Test URL redirect handling with proper HTTP location header"""
        resp = self.client.get("/scholarships/1/apply-redirect?confirm=1")
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers["Location"].startswith("https://"))

    def test_journey_9_invalid_url_rejection(self):
        """TEST 9: Test invalid / malicious URLs are rejected safely"""
        for bad_url in [
            "javascript:alert(document.cookie)",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
            "file:///C:/Windows/System32/drivers/etc/hosts",
            "http://127.0.0.1:5000/admin",
            "http://localhost/secret",
            "http://169.254.169.254/latest/meta-data/"
        ]:
            self.assertFalse(is_valid_http_url(bad_url), f"Should reject: {bad_url}")

    def test_journey_10_mobile_layout(self):
        """TEST 10: Test mobile responsiveness viewport and responsive CSS classes"""
        resp = self.client.get("/scholarships/1")
        self.assertEqual(resp.status_code, 200)
        # Check viewport meta tag in head
        self.assertIn(b'<meta name="viewport" content="width=device-width, initial-scale=1.0">', resp.data)
        # Check responsive flex classes for mobile
        self.assertIn(b"d-flex flex-wrap gap-2", resp.data)


if __name__ == "__main__":
    unittest.main()
