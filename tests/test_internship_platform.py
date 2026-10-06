"""
Automated Test Suite for MPath National Internship Platform.
Validates:
- Normalized Data Models & Backward Compatibility
- Idempotent Ingestion & Deduplication Pipeline
- Multi-Dimensional Matching & Deterministic Eligibility Engine
- AI Retriever Grounding & Function Tools
- Web Route Availability (Explorer, Hubs, Detail Dossier, API, Admin)
- Zero Emoji Integrity Compliance
"""

import unittest
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from extensions import db
from models.internship import Internship, generate_internship_slug
from models.organisation import Organisation
from models.internship_source import InternshipSource
from services.internship.importer import InternshipImporter
from services.internship.national_catalog import NATIONAL_INTERNSHIP_RECORDS
from services.internship.matching_engine import InternshipMatchingEngine
from services.ai.retriever import MPathRetriever


class InternshipPlatformTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

    def test_01_model_and_backward_compatibility(self):
        with self.app.app_context():
            item = Internship.query.first()
            self.assertIsNotNone(item)
            # Verify primary fields
            self.assertTrue(hasattr(item, "title"))
            self.assertTrue(hasattr(item, "slug"))
            self.assertTrue(hasattr(item, "organisation_name"))
            self.assertTrue(hasattr(item, "work_mode"))
            self.assertTrue(hasattr(item, "stipend_min"))
            self.assertTrue(hasattr(item, "application_deadline"))

            # Verify backward compatibility properties
            self.assertEqual(item.company, item.organisation_name)
            self.assertEqual(item.mode, item.work_mode)
            self.assertEqual(item.domain, item.category)
            self.assertIsNotNone(item.apply_link)
            self.assertIsNotNone(item.primary_apply_url)

            # Verify dynamic status method
            status_text, badge_class, icon = item.display_status
            self.assertIn(status_text, ["Open for Applications", "Closing in", "Application Closed"])

    def test_02_idempotent_ingestion_and_deduplication(self):
        with self.app.app_context():
            # Ingesting catalog again should yield duplicates, 0 new items
            res = InternshipImporter.ingest_records(
                records=NATIONAL_INTERNSHIP_RECORDS[:5],
                source_name="Test Ingestion",
                source_code="test-suite",
                dry_run=True
            )
            self.assertEqual(res["new"], 0)
            self.assertEqual(res["duplicates"], 5)
            self.assertEqual(res["invalid"], 0)

    def test_03_deterministic_matching_engine(self):
        with self.app.app_context():
            item = Internship.query.filter_by(category="Technology").first()
            if not item:
                item = Internship.query.first()

            # Profile with perfect skills
            perfect_profile = {
                "degree": "B.Tech CSE",
                "skills": item.skills or "Python, SQL",
                "target_career": "Software Engineer",
                "work_mode": item.work_mode,
                "percentage": 85.0
            }

            match = InternshipMatchingEngine.compute_match(perfect_profile, item)
            self.assertIn("score", match)
            self.assertIn("tier", match)
            self.assertTrue(match["score"] >= 65)
            self.assertTrue(match["eligibility_passed"])
            self.assertIn("why_fits", match["counselling"])

            # Profile failing hard eligibility
            medical_item = Internship.query.filter(Internship.eligible_degrees.ilike("%MBBS%")).first()
            if medical_item:
                non_med_profile = {
                    "degree": "BA History",
                    "skills": "Writing",
                    "percentage": 70.0
                }
                fail_match = InternshipMatchingEngine.compute_match(non_med_profile, medical_item)
                self.assertFalse(fail_match["eligibility_passed"])
                self.assertEqual(fail_match["tier"], "Not Eligible")

    def test_04_ai_retriever_tools(self):
        with self.app.app_context():
            # Search
            search_results = MPathRetriever.search_internships(query="TULIP")
            self.assertTrue(len(search_results) > 0)
            first = search_results[0]
            self.assertIn("title", first)
            self.assertIn("slug", first)
            self.assertIn("organisation", first)
            self.assertIn("dossier_url", first)

            # Details
            details = MPathRetriever.get_internship_details(first["slug"])
            self.assertIsNotNone(details)
            self.assertEqual(details["title"], first["title"])
            self.assertIn("official_apply_url", details)

            # Student Recommendations
            student_profile = {
                "degree": "B.Tech Civil",
                "skills": "AutoCAD, GIS",
                "target_career": "Urban Planner"
            }
            recs = MPathRetriever.find_internships_for_student(student_profile, limit=3)
            self.assertTrue(len(recs) > 0)
            self.assertTrue(recs[0]["match_score"] > 50)

    def test_05_web_routes_and_api(self):
        # 1. Main Explorer
        resp = self.client.get("/internships/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"National Internship Discovery Platform", resp.data)

        # 2. Live API Search
        api_resp = self.client.get("/internships/api/search?search=Python")
        self.assertEqual(api_resp.status_code, 200)
        json_data = api_resp.get_json()
        self.assertTrue(json_data["success"])
        self.assertIn("internships", json_data)

        # 3. Hub Redirects
        govt_resp = self.client.get("/internships/government")
        self.assertEqual(govt_resp.status_code, 302)

        remote_resp = self.client.get("/internships/remote")
        self.assertEqual(remote_resp.status_code, 302)

        # 4. Detail Dossier
        with self.app.app_context():
            sample = Internship.query.first()
            slug = sample.slug

        detail_resp = self.client.get(f"/internships/{slug}")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertIn(sample.title.encode("utf-8"), detail_resp.data)

        # 5. Organisation Profile
        with self.app.app_context():
            org = Organisation.query.first()
            org_slug = org.slug

        org_resp = self.client.get(f"/internships/organisation/{org_slug}")
        self.assertEqual(org_resp.status_code, 200)
        self.assertIn(org.name.encode("utf-8"), org_resp.data)

    def test_06_zero_emojis_in_internship_templates(self):
        """Verify that internship templates contain zero emoji characters."""
        template_files = [
            "templates/internship/list.html",
            "templates/internship/detail.html",
            "templates/internship/organisation.html",
            "templates/internship/tracker.html",
            "templates/admin/internships.html",
            "templates/admin/internships_quality.html",
            "templates/admin/internships_import.html"
        ]

        # Unicode ranges for common emojis
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|"  # SMP
            r"[\u2600-\u26ff]|"          # Misc symbols
            r"[\u2700-\u27bf]"           # Dingbats
        )

        for tf in template_files:
            file_path = os.path.join(os.path.dirname(__file__), "..", tf)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = emoji_pattern.findall(content)
                    self.assertEqual(
                        len(matches),
                        0,
                        f"Found emojis {matches} in {tf}. Emojis are strictly disallowed!"
                    )


if __name__ == "__main__":
    unittest.main()
