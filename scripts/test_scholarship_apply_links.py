"""
scripts/test_scholarship_apply_links.py
Automated end-to-end verification of Scholarship Apply Link & Redirect System.
Covers all 10 required test cases from Section 24 plus security, cycle priority, and analytics.
"""

import os
import sys
import unittest
from datetime import datetime, timedelta

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models.scholarship import (
    Scholarship,
    ScholarshipCycle,
    ScholarshipApplicationClick,
    is_valid_http_url
)


class TestScholarshipApplyLinks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_case_1_valid_direct_application_url(self):
        """CASE 1: Valid direct application URL -> Apply Now enabled and links to exact page"""
        sch = Scholarship.query.filter(Scholarship.official_application_url.isnot(None)).first()
        self.assertIsNotNone(sch, "A valid scholarship record must exist")
        meta = sch.apply_button_meta
        self.assertTrue(meta["is_enabled"])
        self.assertIn("Apply Now", meta["label"])
        self.assertIsNotNone(sch.resolved_application_url)
        self.assertTrue(sch.resolved_application_url.startswith("http"))

        # Test redirect route with confirm=1
        res = self.client.get(f"/scholarships/{sch.id}/apply-redirect?confirm=1")
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers["Location"], sch.resolved_application_url)

    def test_case_2_only_official_website_exists(self):
        """CASE 2: Only official website exists -> No fake Apply button, show Official Website"""
        test_sch = Scholarship(
            title="Dummy Scheme Only Website",
            slug="dummy-scheme-only-website",
            provider="Test Board",
            official_website="https://www.testboard.gov.in",
            official_application_url=None,
            final_application_url=None,
            application_url_status="MISSING",
            verification_status="VERIFIED"
        )
        db.session.add(test_sch)
        db.session.commit()

        meta = test_sch.apply_button_meta
        self.assertFalse(meta["is_enabled"])
        self.assertEqual(meta["label"], "Application Link Unavailable")
        self.assertEqual(test_sch.resolved_official_website, "https://www.testboard.gov.in")
        self.assertIsNone(test_sch.resolved_application_url)

        # Visiting redirect route shows unavailable page rather than redirecting to homepage
        res = self.client.get(f"/scholarships/{test_sch.id}/apply-redirect?confirm=1")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Application Link Unavailable", res.data)
        self.assertIn(b"https://www.testboard.gov.in", res.data)

        db.session.delete(test_sch)
        db.session.commit()

    def test_case_3_application_url_equals_homepage(self):
        """CASE 3: Application URL equals homepage -> Flagged for verification"""
        test_sch = Scholarship(
            title="Suspicious Homepage Scheme",
            slug="suspicious-homepage-scheme",
            provider="Dummy Org",
            official_website="https://www.examplecorp.org",
            official_application_url="https://www.examplecorp.org/",
            application_url_status="NEEDS_VERIFICATION",
            verification_status="NEEDS_REVIEW"
        )
        db.session.add(test_sch)
        db.session.commit()

        self.assertTrue(test_sch.is_homepage_as_app_url)
        self.assertEqual(test_sch.homepage_duplication_warning, "Possible homepage/application URL duplication")

        db.session.delete(test_sch)
        db.session.commit()

    def test_case_4_invalid_url(self):
        """CASE 4: Invalid URL schemes -> Rejected and not redirected"""
        for invalid_url in [
            "javascript:alert(1)",
            "data:text/html,<script>alert(1)</script>",
            "file:///etc/passwd",
            "http://localhost:8080/apply",
            "http://127.0.0.1/steal",
            "#",
            "invalid_scheme://apply"
        ]:
            self.assertFalse(is_valid_http_url(invalid_url), f"Should reject: {invalid_url}")

    def test_case_5_broken_url(self):
        """CASE 5: Broken URL -> Marked BROKEN, Apply button disabled, no redirect"""
        test_sch = Scholarship(
            title="Broken URL Scheme",
            slug="broken-url-scheme",
            provider="Test Body",
            official_website="https://www.officialtest.gov.in",
            official_application_url="https://www.broken-scholarship-url.gov.in/apply",
            application_url_status="BROKEN",
            verification_status="VERIFIED"
        )
        db.session.add(test_sch)
        db.session.commit()

        meta = test_sch.apply_button_meta
        self.assertFalse(meta["is_enabled"])
        self.assertEqual(meta["label"], "Application Link Unavailable")
        self.assertFalse(test_sch.has_direct_apply)

        res = self.client.get(f"/scholarships/{test_sch.id}/apply-redirect?confirm=1")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Application Link Unavailable", res.data)

        db.session.delete(test_sch)
        db.session.commit()

    def test_case_6_expired_scholarship(self):
        """CASE 6: Expired scholarship cycle -> Application Closed badge, blocked redirect"""
        test_sch = Scholarship(
            title="Expired Cycle Scheme",
            slug="expired-cycle-scheme",
            provider="Ministry of Education",
            official_website="https://www.education.gov.in",
            official_application_url="https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
            application_url_status="VALID",
            verification_status="VERIFIED"
        )
        db.session.add(test_sch)
        db.session.flush()

        cycle = ScholarshipCycle(
            scholarship_id=test_sch.id,
            academic_year="2024-25",
            status="CLOSED",
            application_end_date="31-Dec-2024",
            official_application_url="https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
            verification_status="VERIFIED"
        )
        db.session.add(cycle)
        db.session.commit()

        meta = test_sch.apply_button_meta
        self.assertFalse(meta["is_enabled"])
        self.assertEqual(meta["label"], "Application Closed")

        res = self.client.get(f"/scholarships/{test_sch.id}/apply-redirect?confirm=1")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Application Closed", res.data)

        db.session.delete(test_sch)
        db.session.commit()

    def test_case_7_current_cycle_has_application_url(self):
        """CASE 7: Current active cycle has cycle-specific URL -> Priorities current cycle URL"""
        test_sch = Scholarship(
            title="Cycle Priority Scheme",
            slug="cycle-priority-scheme",
            provider="DST",
            official_website="https://dst.gov.in",
            official_application_url="https://fallback.dst.gov.in/apply",
            application_url_status="VALID",
            verification_status="VERIFIED"
        )
        db.session.add(test_sch)
        db.session.flush()

        cycle_2026 = ScholarshipCycle(
            scholarship_id=test_sch.id,
            academic_year="2026-27",
            status="OPEN",
            official_application_url="https://online-inspire.gov.in/she2026/apply",
            verification_status="VERIFIED"
        )
        db.session.add(cycle_2026)
        db.session.commit()

        self.assertEqual(test_sch.resolved_application_url, "https://online-inspire.gov.in/she2026/apply")
        self.assertNotEqual(test_sch.resolved_application_url, "https://fallback.dst.gov.in/apply")

        db.session.delete(test_sch)
        db.session.commit()

    def test_case_8_old_cycle_has_url_but_current_cycle_does_not(self):
        """CASE 8: Old cycle has URL, current cycle has no URL and is UPCOMING -> Does not blindly use old cycle URL"""
        test_sch = Scholarship(
            title="Multi Year Scheme",
            slug="multi-year-scheme",
            provider="State Board",
            official_website="https://state.gov.in",
            official_application_url=None,
            application_url_status="VALID",
            verification_status="VERIFIED"
        )
        db.session.add(test_sch)
        db.session.flush()

        old_cycle = ScholarshipCycle(
            scholarship_id=test_sch.id,
            academic_year="2024-25",
            status="CLOSED",
            official_application_url="https://state.gov.in/2024/apply",
            verification_status="VERIFIED"
        )
        new_cycle = ScholarshipCycle(
            scholarship_id=test_sch.id,
            academic_year="2026-27",
            status="UPCOMING",
            application_start_date="01-Nov-2026",
            official_application_url=None,
            verification_status="VERIFIED"
        )
        db.session.add_all([old_cycle, new_cycle])
        db.session.commit()

        meta = test_sch.apply_button_meta
        # Active cycle is new_cycle (UPCOMING)
        self.assertFalse(meta["is_enabled"])
        self.assertIn("Upcoming", meta["label"])
        # Should not blindly use 2024 cycle URL
        self.assertIsNone(test_sch.resolved_application_url)

        db.session.delete(test_sch)
        db.session.commit()

    def test_case_9_external_government_portal(self):
        """CASE 9: External government portal -> Opens exact registration page, not root homepage"""
        # Central Sector Scheme (ID 1)
        sch = db.session.get(Scholarship, 1)
        self.assertIsNotNone(sch)
        # Check that it points to exact application portal rather than root homepage
        self.assertEqual(sch.resolved_application_url, "https://scholarships.gov.in/ApplicationForm/")
        self.assertNotEqual(sch.resolved_application_url, "https://scholarships.gov.in")
        self.assertEqual(sch.resolved_official_website, "https://www.education.gov.in")

    def test_case_10_unauthorized_url_and_safety(self):
        """CASE 10: Unauthorized URL / Phishing attempts -> Blocked and flagged"""
        self.assertFalse(is_valid_http_url("javascript:void(0)"))
        self.assertFalse(is_valid_http_url("http://localhost:5000/steal"))
        self.assertFalse(is_valid_http_url("http://127.0.0.1:3000/auth"))
        self.assertFalse(is_valid_http_url("ftp://ftp.example.com/apply"))
        self.assertFalse(is_valid_http_url("file:///C:/secrets.txt"))

    def test_analytics_and_departure_warning(self):
        """Verify click analytics tracking without credentials, and departure warning page"""
        sch = Scholarship.query.get(1)
        # Test departure warning page (confirm=0)
        res = self.client.get(f"/scholarships/{sch.id}/apply-redirect")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"External Portal Departure", res.data)
        self.assertIn(b"You are being redirected to the official application portal", res.data)
        self.assertIn(b"Continue to Official Application", res.data)

        # Test analytics recording
        clicks_before = ScholarshipApplicationClick.query.filter_by(scholarship_id=sch.id).count()
        res_redir = self.client.get(f"/scholarships/{sch.id}/apply-redirect?confirm=1&source=test_runner")
        self.assertEqual(res_redir.status_code, 302)
        clicks_after = ScholarshipApplicationClick.query.filter_by(scholarship_id=sch.id).count()
        self.assertGreater(clicks_after, clicks_before)

        latest_click = ScholarshipApplicationClick.query.filter_by(scholarship_id=sch.id).order_by(ScholarshipApplicationClick.id.desc()).first()
        self.assertEqual(latest_click.click_source, "test_runner")
        self.assertEqual(latest_click.target_url, sch.resolved_application_url)

    def test_compatibility_forwarding_routes(self):
        """Verify /scholarship/<id> and /scholarship/<id>/apply forward seamlessly"""
        res = self.client.get("/scholarship/1")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/scholarships/1", res.headers["Location"])

        res_apply = self.client.get("/scholarship/1/apply")
        self.assertEqual(res_apply.status_code, 302)
        self.assertIn("/scholarships/1/apply-redirect", res_apply.headers["Location"])


if __name__ == "__main__":
    unittest.main()
