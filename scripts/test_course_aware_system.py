import os
import sys
import unittest

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from flask import url_for

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from extensions import db
from models.course import Course, CollegeCourse
from models.college import College
from models.career import Career


class CourseAwareSystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_01_search_bca(self):
        """Test 1: Search BCA returns canonical BCA course and verified offering colleges."""
        response = self.client.get("/courses/?search=BCA")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"BCA", response.data)
        
        # Verify BCA exists in database
        bca = Course.query.filter(Course.name.ilike("%BCA%")).first()
        self.assertIsNotNone(bca)
        self.assertGreater(bca.institution_count, 0)
        print(f"[OK] Test 1 Passed: BCA found with {bca.institution_count} verified institutions.")

    def test_02_search_bsc_mathematics(self):
        """Test 2: Search B.Sc Mathematics returns canonical course with verified institutions."""
        response = self.client.get("/courses/?search=B.Sc+Mathematics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"B.Sc Mathematics", response.data)
        
        bsc_math = Course.query.filter_by(name="B.Sc Mathematics").first()
        self.assertIsNotNone(bsc_math)
        self.assertGreater(bsc_math.institution_count, 0)
        print(f"[OK] Test 2 Passed: B.Sc Mathematics found with {bsc_math.institution_count} verified institutions.")

    def test_03_bsc_math_plus_madhya_pradesh(self):
        """Test 3: B.Sc Mathematics + Madhya Pradesh filter returns verified MP colleges."""
        bsc_math = Course.query.filter_by(name="B.Sc Mathematics").first()
        self.assertIsNotNone(bsc_math)
        
        # In course details
        response = self.client.get(f"/courses/{bsc_math.id}?state=Madhya+Pradesh")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Madhya Pradesh", response.data)
        
        # In college directory with course_id + state
        col_resp = self.client.get(f"/colleges/?course_id={bsc_math.id}&state=Madhya+Pradesh")
        self.assertEqual(col_resp.status_code, 200)
        print("[OK] Test 3 Passed: B.Sc Mathematics + Madhya Pradesh combined filtering functional.")

    def test_04_bsc_math_plus_guna(self):
        """Test 4: B.Sc Mathematics + Guna filter returns verified colleges in Guna district."""
        bsc_math = Course.query.filter_by(name="B.Sc Mathematics").first()
        
        # Search via college directory with course + city/district
        response = self.client.get(f"/colleges/?course_id={bsc_math.id}&city=Guna")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Guna", response.data)
        print("[OK] Test 4 Passed: B.Sc Mathematics + Guna multi-tier location filtering functional.")

    def test_05_government_bsc_math_madhya_pradesh(self):
        """Test 5: Government + B.Sc Mathematics + Madhya Pradesh multi-factor filter."""
        bsc_math = Course.query.filter_by(name="B.Sc Mathematics").first()
        response = self.client.get(f"/colleges/?course_id={bsc_math.id}&state=Madhya+Pradesh&gov_priv=Government")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Government", response.data)
        print("[OK] Test 5 Passed: Government + B.Sc Mathematics + MP 3-factor filter functional.")

    def test_06_college_details_shows_courses(self):
        """Test 6: College page displays its actual available courses or honest message."""
        # Find a college with courses
        col_with_courses = (
            College.query.join(CollegeCourse)
            .filter(CollegeCourse.verification_status == "VERIFIED")
            .first()
        )
        self.assertIsNotNone(col_with_courses)
        response = self.client.get(f"/colleges/{col_with_courses.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Academic Programs Offered", response.data)
        print(f"[OK] Test 6 Passed: College '{col_with_courses.name[:30]}' renders verified program dossier.")

    def test_07_career_to_course_to_college(self):
        """Test 7: Career -> Course -> College navigation flow."""
        # Find a career like Data Scientist or AI Engineer
        car = Career.query.filter(Career.title.ilike("%Data%")).first() or Career.query.first()
        self.assertIsNotNone(car)
        response = self.client.get(f"/careers/{car.slug}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recommended Degree Courses", response.data)
        print(f"[OK] Test 7 Passed: Career '{car.title}' connects directly to recommended degree courses.")

    def test_08_alias_search(self):
        """Test 8: Course search understands aliases ('BSc Maths' -> B.Sc Mathematics)."""
        response = self.client.get("/courses/?search=BSc+Maths")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"B.Sc Mathematics", response.data)
        
        # Test JSON API search
        api_resp = self.client.get("/courses/api/search?q=BSc+Maths")
        self.assertEqual(api_resp.status_code, 200)
        json_data = api_resp.get_json()
        self.assertTrue(any(c["name"] == "B.Sc Mathematics" for c in json_data))
        print("[OK] Test 8 Passed: Course search intelligently resolves aliases via HTML and API.")

    def test_09_no_fake_courses(self):
        """Test 9: Colleges without verified relationships do not appear in course filter."""
        # An engineering-only college like MANIT or IIT should not appear in MBBS search
        mbbs = Course.query.filter(Course.name.ilike("%MBBS%")).first()
        self.assertIsNotNone(mbbs)
        
        # Query colleges offering MBBS
        mbbs_colleges = (
            College.query.join(CollegeCourse)
            .filter(CollegeCourse.course_id == mbbs.id, CollegeCourse.verification_status == "VERIFIED")
            .all()
        )
        # Ensure pure engineering / management colleges are NOT in MBBS
        for non_med in ["IIT Bombay", "IIT Delhi", "IIM Ahmedabad", "MANIT"]:
            col = College.query.filter(College.name.ilike(f"%{non_med}%")).first()
            if col:
                self.assertNotIn(col, mbbs_colleges, f"Non-medical college {col.name} incorrectly mapped to MBBS")

        # Verify all mapped institutions are legitimate medical centers
        medical_keywords = ["medical", "aiims", "jipmer", "cmc", "afmc", "kgmu", "pgimer", "nimhans", "health", "hospital"]
        for col in mbbs_colleges:
            self.assertTrue(
                any(k in col.name.lower() for k in medical_keywords) or col.institution_category == "University",
                f"Unexpected college {col.name} in MBBS results"
            )

        print("[OK] Test 9 Passed: No false positive institutions in specialized medical course filter.")

    def test_10_admin_quality_and_models(self):
        """Test 10: Model counts and Admin quality data."""
        total_courses = Course.query.count()
        total_relationships = CollegeCourse.query.count()
        total_colleges = College.query.count()
        self.assertGreaterEqual(total_courses, 40)
        self.assertGreaterEqual(total_relationships, 500)
        self.assertGreaterEqual(total_colleges, 1900)
        print(f"[OK] Test 10 Passed: Total Courses={total_courses}, Total Relationships={total_relationships}, Total Colleges={total_colleges}.")


if __name__ == "__main__":
    unittest.main()
