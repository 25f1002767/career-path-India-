from models.student_profile import StudentProfile
import json
from pathlib import Path


class EligibilityEngine:

    def __init__(self):

        self.path = (
            Path(__file__).resolve().parents[1]
            / "knowledge"
            / "1"
            / "scholarships"
            / "central_scholarships.json"
        )

    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def eligible_scholarships(
        self,
        state,
        percentage,
        income
    ):

        scholarships = self.load()

        results = []

        for s in scholarships:

            state_match = (
                s["state"] == "All India"
                or s["state"].lower() == state.lower()
            )

            percentage_match = (
                percentage >= s["min_percentage"]
            )

            income_match = (
                income <= s["max_income"]
            )

            if state_match and percentage_match and income_match:

                results.append(s)

        return results


eligibility_engine = EligibilityEngine()


def get_student_profile(user_id):
    """
    Return student profile object.
    """

    if not user_id:
        return None

    return StudentProfile.query.filter_by(
        user_id=user_id
    ).first()


def is_career_eligible(profile, career):

    if not profile:
        return True

    if career.education_required:

        education = career.education_required.lower()

        student = (
            profile.current_class or ""
        ).lower()

        if student not in education:
            return False

    return True


def is_exam_eligible(profile, exam):

    if not profile:
        return True

    qualification = (
        exam.qualification or ""
    ).lower()

    student = (
        profile.current_class or ""
    ).lower()

    if qualification:

        if student not in qualification:
            return False

    return True


def is_scholarship_eligible(profile, scholarship):

    if not profile:
        return True

    eligibility = (
        scholarship.eligibility or ""
    ).lower()

    student = (
        profile.current_class or ""
    ).lower()

    if eligibility:

        if student not in eligibility:
            return False

    return True


def is_internship_eligible(profile, internship):

    if not profile:
        return True

    eligibility = (
        internship.eligibility or ""
    ).lower()

    student = (
        profile.current_class or ""
    ).lower()

    if eligibility:

        if student not in eligibility:
            return False

    return True