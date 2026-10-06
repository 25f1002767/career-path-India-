import re
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from models.student_profile import StudentProfile
from models.user import User


class EligibilityEngine:
    """
    Legacy scholarship eligibility engine retained for backwards compatibility.
    """
    def __init__(self):
        self.path = (
            Path(__file__).resolve().parents[1]
            / "knowledge"
            / "1"
            / "scholarships"
            / "central_scholarships.json"
        )

    def load(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def eligible_scholarships(self, state, percentage, income):
        scholarships = self.load()
        results = []
        for s in scholarships:
            state_match = (
                s.get("state") == "All India"
                or (s.get("state") or "").lower() == (state or "").lower()
            )
            percentage_match = percentage >= s.get("min_percentage", 0)
            income_match = income <= s.get("max_income", float('inf'))
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
    return StudentProfile.query.filter_by(user_id=user_id).first()


class OpportunityEligibilityEvaluator:
    """
    Deterministic Multi-Factor Eligibility Engine for National Examinations and Career Opportunities.
    Zero hallucination. Deterministic rules evaluating Education Level, Degree, Stream, Age, State/Domicile,
    Gender, and Category criteria.
    Outputs: ELIGIBLE, LIKELY_ELIGIBLE, NOT_ELIGIBLE, UNKNOWN, NEEDS_REVIEW.
    """

    EDUCATION_HIERARCHY = {
        "10th": 1,
        "class 10": 1,
        "matriculation": 1,
        "12th": 2,
        "class 12": 2,
        "intermediate": 2,
        "higher secondary": 2,
        "iti": 2,
        "diploma": 3,
        "polytechnic": 3,
        "graduate": 4,
        "ug": 4,
        "bachelor": 4,
        "b.sc": 4,
        "bsc": 4,
        "b.tech": 4,
        "btech": 4,
        "b.e": 4,
        "be": 4,
        "ba": 4,
        "b.com": 4,
        "bcom": 4,
        "bca": 4,
        "bba": 4,
        "llb": 4,
        "mbbs": 4,
        "bds": 4,
        "postgraduate": 5,
        "pg": 5,
        "master": 5,
        "m.sc": 5,
        "msc": 5,
        "m.tech": 5,
        "mtech": 5,
        "ma": 5,
        "m.com": 5,
        "mcom": 5,
        "mca": 5,
        "mba": 5,
        "llm": 5,
        "phd": 6,
        "doctorate": 6
    }

    @classmethod
    def evaluate(cls, opportunity, student_input: Any) -> Dict[str, Any]:
        """
        Evaluates opportunity eligibility against student profile or dictionary input.
        """
        # 1. Normalize student input
        data = cls._normalize_student_data(student_input)

        reasons = []
        disqualifications = []
        missing_info = []
        criteria = {}

        # ---------------------------------------------------------------------
        # A. AGE EVALUATION
        # ---------------------------------------------------------------------
        age = data.get("age")
        age_min = getattr(opportunity, "age_min", None)
        age_max = getattr(opportunity, "age_max", None)
        age_relax = getattr(opportunity, "age_relaxation", "") or ""
        category = (data.get("category") or "General").upper()

        if age is not None:
            effective_max = age_max
            if age_max:
                if category in ("SC", "ST") and ("SC" in age_relax or "ST" in age_relax):
                    effective_max += 5
                elif "OBC" in category and "OBC" in age_relax:
                    effective_max += 3
                elif data.get("is_pwd") and "PW" in age_relax.upper():
                    effective_max += 10

            if age_min and age < age_min:
                disqualifications.append(f"Age {age} is below minimum requirement of {age_min} years.")
                criteria["age"] = {"status": "FAIL", "detail": f"Below min age ({age_min})"}
            elif effective_max and age > effective_max:
                disqualifications.append(f"Age {age} exceeds maximum limit of {effective_max} years (including category relaxation).")
                criteria["age"] = {"status": "FAIL", "detail": f"Exceeds max age ({effective_max})"}
            else:
                reasons.append(f"Age ({age} yrs) satisfies age requirements ({age_min or 'Any'} to {effective_max or 'Any'}).")
                criteria["age"] = {"status": "PASS", "detail": f"Within permitted age limit"}
        else:
            if age_min or age_max:
                missing_info.append("Age not provided (Required: " + f"{age_min or ''}-{age_max or ''} yrs)")
                criteria["age"] = {"status": "UNKNOWN", "detail": "Age not provided"}
            else:
                criteria["age"] = {"status": "PASS", "detail": "No strict age limit specified"}

        # ---------------------------------------------------------------------
        # B. EDUCATION LEVEL & DEGREE EVALUATION
        # ---------------------------------------------------------------------
        student_edu = (data.get("education_level") or data.get("current_class") or data.get("course") or "").lower()
        exam_qual = (getattr(opportunity, "qualification", "") or getattr(opportunity, "minimum_qualification", "") or "").lower()
        exam_edu_level = (getattr(opportunity, "education_level", "") or "").lower()

        edu_rank_student = cls._get_education_rank(student_edu)
        edu_rank_exam = cls._get_education_rank(exam_edu_level or exam_qual)

        if edu_rank_student and edu_rank_exam:
            if edu_rank_student >= edu_rank_exam:
                reasons.append(f"Educational level satisfies minimum requirement ({getattr(opportunity, 'minimum_qualification') or getattr(opportunity, 'qualification') or 'Required level'}).")
                criteria["education"] = {"status": "PASS", "detail": "Level satisfied"}
            else:
                disqualifications.append(f"Current education level ({student_edu}) is below minimum requirement ({getattr(opportunity, 'minimum_qualification') or getattr(opportunity, 'qualification')}).")
                criteria["education"] = {"status": "FAIL", "detail": "Insufficient level"}
        elif not student_edu:
            missing_info.append("Education level/class not specified.")
            criteria["education"] = {"status": "UNKNOWN", "detail": "Education level unknown"}
        else:
            # Fuzzy check if exact rank unknown
            if any(term in exam_qual for term in ["any discipline", "any stream", "recognized university"]):
                if any(g in student_edu for g in ["bachelor", "degree", "graduate", "ug", "b.sc", "btech", "b.com", "ba"]):
                    reasons.append(f"Degree satisfies 'Graduate in Any Discipline' requirement.")
                    criteria["education"] = {"status": "PASS", "detail": "Degree recognized"}
                else:
                    criteria["education"] = {"status": "UNKNOWN", "detail": "Requires verification of graduation"}
            else:
                criteria["education"] = {"status": "PASS", "detail": "Open qualification"}

        # ---------------------------------------------------------------------
        # C. ACADEMIC STREAM & SUBJECT EVALUATION
        # ---------------------------------------------------------------------
        student_stream = (data.get("stream") or "").lower()
        student_subjects = [s.lower() for s in (data.get("subjects") or [])]
        exam_streams = (getattr(opportunity, "streams", "") or "").lower()
        exam_specialisation = (getattr(opportunity, "specialisation", "") or "").lower()

        if exam_streams and "any" not in exam_streams and exam_streams != "":
            if not student_stream and not student_subjects:
                missing_info.append(f"Academic stream not provided (Required: {getattr(opportunity, 'streams')})")
                criteria["stream"] = {"status": "UNKNOWN", "detail": "Stream not provided"}
            else:
                # Check for stream match
                stream_matched = False
                if "science" in exam_streams and any(s in student_stream for s in ["science", "pcm", "pcb", "pcmb", "math"]):
                    stream_matched = True
                elif "engineering" in exam_streams and any(s in student_stream for s in ["engineering", "tech", "b.tech", "b.e"]):
                    stream_matched = True
                elif "math" in exam_streams and (any("math" in s for s in student_subjects) or "math" in student_stream):
                    stream_matched = True
                elif "commerce" in exam_streams and "commerce" in student_stream:
                    stream_matched = True
                elif any(word in student_stream for word in exam_streams.replace(",", " ").split() if len(word) > 3):
                    stream_matched = True

                if stream_matched:
                    reasons.append(f"Stream ({data.get('stream')}) aligns with required eligibility ({getattr(opportunity, 'streams')}).")
                    criteria["stream"] = {"status": "PASS", "detail": "Stream aligned"}
                else:
                    disqualifications.append(f"Stream mismatch: Required '{getattr(opportunity, 'streams')}', student has '{data.get('stream')}'.")
                    criteria["stream"] = {"status": "FAIL", "detail": "Stream mismatch"}
        else:
            criteria["stream"] = {"status": "PASS", "detail": "Open to any stream"}

        # ---------------------------------------------------------------------
        # D. STATE & DOMICILE EVALUATION
        # ---------------------------------------------------------------------
        student_state = (data.get("state") or "").lower()
        exam_state = (getattr(opportunity, "state", "") or "All India").lower()
        exam_jurisdiction = (getattr(opportunity, "national_or_state", "National") or "National").lower()
        domicile_req = (getattr(opportunity, "domicile_requirement", "") or "").lower()

        if exam_jurisdiction == "state" and exam_state != "all india":
            if not student_state:
                missing_info.append(f"Domicile state not provided (Exam organized for: {getattr(opportunity, 'state')})")
                criteria["state"] = {"status": "UNKNOWN", "detail": "State unknown"}
            elif exam_state in student_state or student_state in exam_state:
                reasons.append(f"Resident of {getattr(opportunity, 'state')} fulfilling state recruitment scope.")
                criteria["state"] = {"status": "PASS", "detail": "Domicile matched"}
            else:
                if "all india" in domicile_req or "open to all" in domicile_req:
                    reasons.append(f"National applicants eligible under General/Unreserved quota for {getattr(opportunity, 'state')}.")
                    criteria["state"] = {"status": "PASS", "detail": "Open to All India under UR quota"}
                else:
                    criteria["state"] = {"status": "UNKNOWN", "detail": f"State specific ({getattr(opportunity, 'state')})"}
        else:
            criteria["state"] = {"status": "PASS", "detail": "National / All India scope"}

        # ---------------------------------------------------------------------
        # E. GENDER EVALUATION
        # ---------------------------------------------------------------------
        student_gender = (data.get("gender") or "").lower()
        exam_gender = (getattr(opportunity, "gender_eligibility", "All") or "All").lower()

        if exam_gender not in ["all", "any", ""]:
            if not student_gender:
                criteria["gender"] = {"status": "UNKNOWN", "detail": "Gender not specified"}
            elif student_gender in exam_gender:
                reasons.append(f"Gender criteria satisfied ({getattr(opportunity, 'gender_eligibility')}).")
                criteria["gender"] = {"status": "PASS", "detail": "Gender satisfied"}
            else:
                disqualifications.append(f"Opportunity specifies {getattr(opportunity, 'gender_eligibility')}.")
                criteria["gender"] = {"status": "FAIL", "detail": "Gender restriction"}
        else:
            criteria["gender"] = {"status": "PASS", "detail": "Open to all genders"}

        # ---------------------------------------------------------------------
        # SYNTHESIS & FINAL DETERMINATION
        # ---------------------------------------------------------------------
        if disqualifications:
            final_status = "NOT_ELIGIBLE"
            score = 15
        elif missing_info and not reasons:
            final_status = "UNKNOWN"
            score = 50
        elif missing_info and reasons:
            final_status = "LIKELY_ELIGIBLE"
            score = 75
        elif reasons and not disqualifications:
            final_status = "ELIGIBLE"
            score = 95
        else:
            final_status = "UNKNOWN"
            score = 50

        return {
            "status": final_status,
            "score": score,
            "is_eligible": final_status in ["ELIGIBLE", "LIKELY_ELIGIBLE"],
            "reasons": reasons,
            "not_eligible_reasons": disqualifications,
            "disqualifications": disqualifications,
            "missing_info": missing_info,
            "criteria_breakdown": criteria
        }

    @classmethod
    def _normalize_student_data(cls, student_input: Any) -> Dict[str, Any]:
        data = {}
        if not student_input:
            return data

        if isinstance(student_input, dict):
            data = student_input.copy()
        elif hasattr(student_input, "__dict__"):
            # Check if User or StudentProfile
            if hasattr(student_input, "current_class"):
                data["current_class"] = student_input.current_class
                data["state"] = student_input.state
                data["district"] = student_input.district
                data["career_goal"] = student_input.career_goal
                if hasattr(student_input, "user") and student_input.user:
                    u = student_input.user
                    data["stream"] = u.stream
                    data["course"] = u.course
                    data["class_grade"] = u.class_grade
            elif hasattr(student_input, "role"):  # User object
                data["state"] = student_input.state
                data["stream"] = student_input.stream
                data["course"] = student_input.course
                data["class_grade"] = student_input.class_grade
                if student_input.profile:
                    data["current_class"] = student_input.profile.current_class

        # Parse age from string if needed
        if "age" in data and isinstance(data["age"], str):
            digits = re.findall(r"\d+", data["age"])
            if digits:
                data["age"] = int(digits[0])

        return data

    @classmethod
    def _get_education_rank(cls, text: str) -> Optional[int]:
        if not text:
            return None
        text_lower = text.lower()
        for key, rank in cls.EDUCATION_HIERARCHY.items():
            if key in text_lower:
                return rank
        return None


def is_exam_eligible(profile, exam) -> bool:
    """
    Deterministic examination eligibility evaluation replacing legacy substring check.
    """
    if not profile:
        return True
    res = OpportunityEligibilityEvaluator.evaluate(exam, profile)
    return res["status"] in ["ELIGIBLE", "LIKELY_ELIGIBLE", "UNKNOWN"]


def is_career_eligible(profile, career):
    if not profile:
        return True
    if career.education_required:
        education = career.education_required.lower()
        student = (profile.current_class or "").lower()
        if student and student not in education:
            return False
    return True


def is_scholarship_eligible(profile, scholarship):
    if not profile:
        return True
    eligibility = (scholarship.eligibility or "").lower()
    student = (profile.current_class or "").lower()
    if eligibility and student and student not in eligibility:
        return False
    return True


def is_internship_eligible(profile, internship):
    if not profile:
        return True
    eligibility = (internship.eligibility or "").lower()
    student = (profile.current_class or "").lower()
    if eligibility and student and student not in eligibility:
        return False
    return True