"""
Deterministic Multi-Dimensional Internship Matching & Eligibility Engine.
Evaluates student academic profile, skills, career interests, and work preferences
against verified internship opportunity specifications.
Outputs structured breakdown and transparent counselling reasoning.
"""

from typing import Dict, Any, List, Optional
import re
from models.internship import Internship
from models.user import User


class InternshipMatchingEngine:
    """
    Deterministic scoring and counselling explanation engine.
    """

    @staticmethod
    def _normalize_tokens(text: Optional[str]) -> set:
        if not text:
            return set()
        clean = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = set(t.strip() for t in clean.split() if len(t.strip()) > 1)
        return tokens

    @staticmethod
    def _extract_phrases(text: Optional[str]) -> List[str]:
        if not text:
            return []
        items = re.split(r"[,/|;]+", text)
        return [i.strip() for i in items if i.strip()]

    @classmethod
    def evaluate_eligibility(cls, student_profile: Dict[str, Any], internship: Internship) -> Dict[str, Any]:
        """
        Hard deterministic eligibility checks.
        """
        reasons = []
        is_eligible = True

        # 1. Degree / Qualification check
        req_degrees = (internship.eligible_degrees or "").lower()
        student_degree = (student_profile.get("degree") or student_profile.get("qualification") or "").lower()

        if req_degrees and "any" not in req_degrees and student_degree:
            req_tokens = cls._normalize_tokens(req_degrees)
            std_tokens = cls._normalize_tokens(student_degree)
            # Check for any match in degrees
            has_degree_match = bool(req_tokens & std_tokens) or any(d in student_degree for d in ["b.tech", "btech", "b.e", "be", "bca", "mca", "b.sc", "bsc"] if d in req_degrees)
            if not has_degree_match:
                # If specifically restrictive degree
                if any(specific in req_degrees for specific in ["mbbs", "bds", "ll.b", "law"]):
                    is_eligible = False
                    reasons.append(f"Requires specific academic qualification: {internship.eligible_degrees}")
                else:
                    reasons.append(f"Preferred degrees are {internship.eligible_degrees}; your degree is {student_profile.get('degree')}")

        # 2. Minimum Percentage / CGPA check
        min_pct = internship.minimum_percentage or 0.0
        student_pct = float(student_profile.get("percentage") or student_profile.get("cgpa_percent") or 100.0)
        if min_pct > 0.0 and student_pct < min_pct:
            is_eligible = False
            reasons.append(f"Requires minimum academic score of {min_pct}%, your score is {student_pct}%.")

        return {
            "is_eligible": is_eligible,
            "reasons": reasons
        }

    @classmethod
    def compute_match(cls, student_profile: Dict[str, Any], internship: Internship) -> Dict[str, Any]:
        """
        Computes 5-dimensional deterministic score:
        1. Eligibility (25%)
        2. Skill Alignment (35%)
        3. Career & Domain Alignment (20%)
        4. Work Mode & Location Fit (10%)
        5. Availability & Duration Fit (10%)
        """
        # --- 1. Eligibility Check (25 pts) ---
        elig_res = cls.evaluate_eligibility(student_profile, internship)
        elig_score = 25 if elig_res["is_eligible"] else 5

        # --- 2. Skill Match (35 pts) ---
        internship_skills = cls._extract_phrases(internship.technical_skills or internship.skills)
        if not internship_skills:
            internship_skills = ["Problem Solving", "Communication", "Fundamentals"]

        student_skills_raw = student_profile.get("skills") or []
        if isinstance(student_skills_raw, str):
            student_skills = cls._extract_phrases(student_skills_raw)
        else:
            student_skills = [str(s) for s in student_skills_raw]

        matched_skills = []
        missing_skills = []

        std_skills_lower = {s.lower() for s in student_skills}
        for iskill in internship_skills:
            iskill_low = iskill.lower()
            if any(iskill_low in ss or ss in iskill_low for ss in std_skills_lower):
                matched_skills.append(iskill)
            else:
                missing_skills.append(iskill)

        skill_ratio = len(matched_skills) / max(len(internship_skills), 1)
        skill_score = round(skill_ratio * 35)

        # --- 3. Career & Domain Fit (20 pts) ---
        career_interest = (student_profile.get("target_career") or student_profile.get("career_interest") or "").lower()
        domain = (internship.category or internship.industry or "").lower()
        title_lower = internship.title.lower()

        career_score = 10  # default baseline
        if career_interest:
            ci_tokens = cls._normalize_tokens(career_interest)
            dom_tokens = cls._normalize_tokens(domain)
            title_tokens = cls._normalize_tokens(title_lower)
            if ci_tokens & title_tokens:
                career_score = 20
            elif ci_tokens & dom_tokens:
                career_score = 16
            else:
                career_score = 8

        # --- 4. Work Mode & Location Fit (10 pts) ---
        pref_mode = (student_profile.get("work_mode") or "Any").lower()
        int_mode = (internship.work_mode or "Hybrid").lower()

        mode_score = 5
        if pref_mode in ("any", "all") or int_mode == "remote":
            mode_score = 10
        elif pref_mode == int_mode:
            mode_score = 10
        elif "hybrid" in (pref_mode, int_mode):
            mode_score = 7

        # Location check
        student_city = (student_profile.get("city") or "").lower()
        student_state = (student_profile.get("state") or "").lower()
        int_city = (internship.city or "").lower()
        int_state = (internship.state or "").lower()

        if int_mode == "remote" or internship.is_pan_india or "all india" in (int_city, int_state):
            loc_fit = "Flexible / Remote"
        elif student_city and student_city in int_city:
            loc_fit = "Local Match"
            mode_score = min(mode_score + 2, 10)
        elif student_state and student_state in int_state:
            loc_fit = "State Match"
            mode_score = min(mode_score + 1, 10)
        else:
            loc_fit = f"{internship.city or 'Onsite'}, {internship.state or ''}"

        # --- 5. Duration & Availability Fit (10 pts) ---
        duration_score = 10  # standard internship terms align with college semesters

        # --- Total Score ---
        total_score = min(elig_score + skill_score + career_score + mode_score + duration_score, 100)

        # Determine Tier
        if not elig_res["is_eligible"]:
            tier = "Not Eligible"
            tier_class = "danger"
        elif total_score >= 80:
            tier = "Strong Match"
            tier_class = "success"
        elif total_score >= 65:
            tier = "Good Match"
            tier_class = "info"
        elif total_score >= 50:
            tier = "Possible Match"
            tier_class = "warning"
        else:
            tier = "Needs Review"
            tier_class = "secondary"

        # Counselling Explanation synthesis
        why_fits = []
        if matched_skills:
            why_fits.append(f"Your proficiency in {', '.join(matched_skills[:3])} aligns directly with role requirements.")
        if career_interest and career_score >= 15:
            why_fits.append(f"Direct alignment with your career goal in {student_profile.get('target_career')}.")
        if internship.work_mode == "Remote":
            why_fits.append("100% Remote flexibility allows balance with ongoing academic coursework.")
        if internship.academic_credit_available:
            why_fits.append("Statutory academic credits and official certificate available.")

        if not why_fits:
            why_fits.append(f"Provides foundational exposure in {internship.category or 'industry'} at {internship.organisation_name}.")

        next_steps = []
        if missing_skills:
            next_steps.append(f"Brush up on {', '.join(missing_skills[:2])} before submitting your application.")
        if internship.application_deadline:
            next_steps.append(f"Submit before the deadline: {internship.deadline_text}.")

        return {
            "score": total_score,
            "tier": tier,
            "tier_class": tier_class,
            "breakdown": {
                "eligibility_score": elig_score,
                "skill_score": skill_score,
                "career_score": career_score,
                "mode_score": mode_score,
                "duration_score": duration_score
            },
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "skill_match_percentage": round(skill_ratio * 100),
            "location_fit": loc_fit,
            "eligibility_passed": elig_res["is_eligible"],
            "eligibility_reasons": elig_res["reasons"],
            "counselling": {
                "why_fits": why_fits,
                "potential_gaps": missing_skills[:3],
                "recommended_next_step": " ".join(next_steps)
            }
        }
