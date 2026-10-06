import unittest
from datetime import date
from app import app
from extensions import db
from models.user import User
from models.exam import GovernmentExam
from models.exam_cycle import ExamCycle
from models.opportunity_source import OpportunitySource
from models.opportunity_tracker import StudentOpportunityTracker
from models.student_profile import StudentProfile
from services.eligibility_engine import OpportunityEligibilityEvaluator, is_exam_eligible
from services.opportunity_engine import discover_opportunities
from services.ai.tools import ToolExecutor
from services.ai.retriever import MPathRetriever
from services.url_validator import URLValidatorService


class TestOpportunityPlatform(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_01_database_and_models(self):
        """Test models exist, relationships are functional, and properties work."""
        total_exams = GovernmentExam.query.count()
        self.assertGreater(total_exams, 0, "Database should contain verified examinations")

        total_sources = OpportunitySource.query.count()
        self.assertGreater(total_sources, 0, "Database should contain statutory sources")

        exam = GovernmentExam.query.first()
        self.assertIsNotNone(exam.exam_name)
        self.assertEqual(exam.name, exam.exam_name)
        self.assertIsNotNone(exam.display_status)
        self.assertEqual(len(exam.display_status), 3)

        # Verify cycles relationship
        cycle_count = ExamCycle.query.count()
        self.assertGreater(cycle_count, 0, "Database should contain recorded exam cycles")

    def test_02_deterministic_eligibility_bsc_maths_mp(self):
        """Test deterministic eligibility for B.Sc Mathematics student from Madhya Pradesh."""
        student = {
            "education_level": "Graduate / UG",
            "stream": "Mathematics",
            "course": "B.Sc Mathematics",
            "state": "Madhya Pradesh",
            "age": 22,
            "category": "General"
        }

        # UPSC Civil Services
        upsc = GovernmentExam.query.filter(GovernmentExam.exam_name.ilike("%UPSC Civil Services%")).first()
        if upsc:
            res = OpportunityEligibilityEvaluator.evaluate(upsc, student)
            self.assertIn(res["status"], ["ELIGIBLE", "LIKELY_ELIGIBLE"])
            self.assertGreaterEqual(res["score"], 80)
            self.assertTrue(any("satisfies" in r.lower() or "graduate" in r.lower() for r in res["reasons"]))

        # MPPSC State Services
        mppsc = GovernmentExam.query.filter(GovernmentExam.exam_name.ilike("%MPPSC%")).first()
        if mppsc:
            res = OpportunityEligibilityEvaluator.evaluate(mppsc, student)
            self.assertIn(res["status"], ["ELIGIBLE", "LIKELY_ELIGIBLE"])
            self.assertGreaterEqual(res["score"], 80)

    def test_03_disqualification_underage_and_underqualified(self):
        """Test deterministic rejection for student who does not meet hard criteria."""
        underage_student = {
            "education_level": "10th",
            "age": 15,
            "category": "General"
        }
        upsc = GovernmentExam.query.filter(GovernmentExam.exam_name.ilike("%UPSC Civil Services%")).first()
        if upsc:
            res = OpportunityEligibilityEvaluator.evaluate(upsc, underage_student)
            self.assertEqual(res["status"], "NOT_ELIGIBLE")
            self.assertGreater(len(res["disqualifications"]), 0)

    def test_04_opportunity_engine_discovery(self):
        """Test discover_opportunities with and without student profile."""
        # Unauthenticated / empty profile
        opps = discover_opportunities(None)
        self.assertIsInstance(opps, list)
        self.assertGreater(len(opps), 0)

        # Profile with B.Sc Maths MP
        mock_p = StudentProfile(current_class="B.Sc Mathematics", career_goal="Civil Services")
        mock_p.state = "Madhya Pradesh"
        filtered_opps = discover_opportunities(mock_p)
        self.assertIsInstance(filtered_opps, list)
        # Check that matched exams have valid scores and reasons
        exam_opps = [o for o in filtered_opps if o["type"] == "Government Exam"]
        self.assertGreater(len(exam_opps), 0)
        for eo in exam_opps[:5]:
            self.assertGreaterEqual(eo["match"], 50)
            self.assertIsInstance(eo["reasons"], list)

    def test_05_ai_mentor_tools_execution(self):
        """Test that AI function tools return grounded records without fabrication."""
        # Tool: find_opportunities_for_student
        res = ToolExecutor.execute("find_opportunities_for_student", {
            "course": "B.Sc Mathematics",
            "state": "Madhya Pradesh",
            "age": 22
        })
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), 0)
        first_item = res[0]
        self.assertIn("name", first_item)
        self.assertIn("official_portal", first_item)
        self.assertIn("reasons", first_item)

        # Tool: get_exam_details
        dossier = ToolExecutor.execute("get_exam_details", {"exam_identifier": "UPSC CSE"})
        self.assertIsNotNone(dossier)
        self.assertIn("exam_name", dossier)
        self.assertIn("official_portal", dossier)

    def test_06_url_validator(self):
        """Test URL validation service flags invalid and non-HTTPS links."""
        res_valid = URLValidatorService.validate_url("https://upsc.gov.in")
        self.assertTrue(res_valid["is_valid"])
        self.assertTrue(res_valid["is_https"])
        self.assertEqual(res_valid["status"], "VALID")

        res_invalid = URLValidatorService.validate_url("not-a-valid-url")
        self.assertFalse(res_invalid["is_valid"])

    def test_07_public_routes_status_200(self):
        """Test all exam routes return 200 OK."""
        # Catalog list
        resp = self.client.get("/exams/")
        self.assertEqual(resp.status_code, 200)

        # First exam detail
        first_exam = GovernmentExam.query.first()
        if first_exam:
            resp_detail = self.client.get(f"/exams/{first_exam.id}")
            self.assertEqual(resp_detail.status_code, 200)

        # Calendar
        resp_cal = self.client.get("/exams/calendar")
        self.assertEqual(resp_cal.status_code, 200)

        # Eligibility finder
        resp_elig = self.client.get("/exams/eligibility")
        self.assertEqual(resp_elig.status_code, 200)

        # Comparison tool
        resp_comp = self.client.get("/exams/compare?id=1&id=2")
        self.assertEqual(resp_comp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
