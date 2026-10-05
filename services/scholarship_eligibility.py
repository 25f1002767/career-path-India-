"""
services/scholarship_eligibility.py
==============================================================================
MPath National Scholarship Eligibility & Scoring Engine
==============================================================================
Deterministic, explainable rule engine that evaluates student attributes
against scholarship criteria. Provides transparent reasons ("Why Am I Eligible?"),
identifies document prerequisites, and detects potential blockers.
==============================================================================
"""

import re
from typing import Dict, Any, List, Tuple


class ScholarshipEligibilityEngine:

    @staticmethod
    def parse_income_to_float(val: Any) -> float:
        """Parse income strings like '250000', '2.5 Lakh', '₹ 8,00,000' into a float"""
        if val is None or val == "":
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)

        val_str = str(val).lower().replace(",", "").replace("₹", "").replace("rs.", "").replace("inr", "").strip()
        if "lakh" in val_str or "lac" in val_str:
            num_match = re.search(r"(\d+(\.\d+)?)", val_str)
            if num_match:
                return float(num_match.group(1)) * 100000.0
        num_match = re.search(r"(\d+(\.\d+)?)", val_str)
        if num_match:
            return float(num_match.group(1))
        return 0.0

    @classmethod
    def evaluate(cls, scholarship, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a single scholarship against student attributes.
        Returns:
            {
                "status": "ELIGIBLE" | "LIKELY_ELIGIBLE" | "PARTIALLY_MATCHED" | "NOT_ELIGIBLE",
                "fit_score": int (0-100),
                "positive_signals": list[str],
                "warnings": list[str],
                "blockers": list[str],
                "documents_needed": list[str],
                "action_step": str
            }
        """
        score = 60  # Base potential match
        positives = []
        warnings = []
        blockers = []

        # 1. State / Domicile Check
        student_state = (student_data.get("state") or "").strip()
        scholarship_state = (scholarship.state or scholarship.domicile_requirement or "").strip()
        nat_or_state = (scholarship.national_or_state or "National").strip()

        if scholarship_state and scholarship_state not in ["All India", "National", "All", "India", ""]:
            if student_state:
                if student_state.lower() == scholarship_state.lower():
                    positives.append(f"Domicile matched: Valid for permanent residents of {scholarship_state}.")
                    score += 15
                else:
                    blockers.append(f"State restriction: Exclusive to residents of {scholarship_state} (your stated state: {student_state}).")
                    score -= 40
            else:
                warnings.append(f"State domicile required: Restricted to {scholarship_state}. (Verify your state in profile).")
                score -= 10
        else:
            positives.append("Pan-India Coverage: Open to eligible Indian nationals across all States and UTs.")
            score += 10

        # 2. Gender Check
        gender_req = (scholarship.gender_eligibility or "All").strip().lower()
        student_gender = (student_data.get("gender") or "").strip().lower()

        if gender_req in ["female only", "girls only", "female", "women"]:
            if student_gender:
                if student_gender in ["female", "girl", "woman"]:
                    positives.append("Gender eligibility matched: Special scheme for female candidates.")
                    score += 15
                else:
                    blockers.append("Gender eligibility: Exclusively designated for girl / female students.")
                    score -= 50
            else:
                warnings.append("Gender eligibility: Applicable exclusively to female students.")
                score -= 10
        elif gender_req in ["transgender only", "transgender"]:
            if student_gender == "transgender":
                positives.append("Gender eligibility: Designated for transgender students.")
                score += 20
            else:
                blockers.append("Reserved for transgender students.")
                score -= 50

        # 3. Family Income Check
        income_limit = scholarship.family_income_limit
        student_income = cls.parse_income_to_float(student_data.get("family_income"))

        if income_limit and income_limit > 0:
            formatted_limit = f"₹{income_limit:,.0f}" if income_limit < 10000000 else f"₹{income_limit/100000:.1f} Lakh"
            if student_income > 0:
                if student_income <= income_limit:
                    positives.append(f"Means criterion satisfied: Your family income (₹{student_income:,.0f}) is within the statutory limit of {formatted_limit}.")
                    score += 15
                else:
                    blockers.append(f"Income threshold exceeded: Scheme requires family annual income ≤ {formatted_limit} (reported: ₹{student_income:,.0f}).")
                    score -= 40
            else:
                warnings.append(f"Income limit: Requires annual family income ≤ {formatted_limit}. (Requires Competent Revenue Authority Certificate).")
                score -= 5

        # 4. Social Category Check
        cat_req = (scholarship.category_requirement or "All").strip().upper()
        student_cat = (student_data.get("category") or "").strip().upper()

        if cat_req not in ["ALL", "GENERAL", "ANY", "OPEN", ""]:
            req_cats = [c.strip() for c in cat_req.replace("/", ",").split(",") if c.strip()]
            if student_cat:
                if any(c in student_cat or student_cat in c for c in req_cats):
                    positives.append(f"Category requirement satisfied: Applicable for {cat_req} students.")
                    score += 15
                else:
                    blockers.append(f"Category requirement: Exclusively designated for {cat_req} candidates (profile: {student_cat}).")
                    score -= 45
            else:
                warnings.append(f"Category eligibility: Designated for {cat_req} students. (Valid caste certificate required).")
                score -= 5
        else:
            positives.append("Open Category: No restrictive caste or communal reservation prerequisite.")

        # 5. Academic Performance / Percentage Check
        min_pct = scholarship.percentage_requirement
        student_pct = student_data.get("percentage")
        if student_pct is not None and student_pct != "":
            try:
                s_pct = float(str(student_pct).replace("%", "").strip())
                if min_pct and min_pct > 0:
                    if s_pct >= min_pct:
                        positives.append(f"Academic threshold satisfied: Your score of {s_pct:.1f}% satisfies the minimum {min_pct:.1f}% benchmark.")
                        score += 15
                    else:
                        blockers.append(f"Academic percentage: Requires minimum {min_pct:.1f}% in qualifying examination (current: {s_pct:.1f}%).")
                        score -= 35
                else:
                    positives.append(f"Qualifying marks: Your {s_pct:.1f}% satisfies basic merit requirements.")
                    score += 5
            except ValueError:
                pass
        elif min_pct and min_pct > 0:
            warnings.append(f"Merit requirement: Requires at least {min_pct:.1f}% in qualifying examination.")

        # 6. Education Level & Course Check
        edu_req = (scholarship.education_level or "").strip().lower()
        student_class = (student_data.get("class_grade") or student_data.get("education_level") or "").strip().lower()
        student_course = (student_data.get("course") or "").strip().lower()

        if edu_req and edu_req not in ["any", "all", "open"]:
            # Check for keyword matches
            is_edu_matched = False
            if "undergraduate" in edu_req or "ug" in edu_req or "bachelor" in edu_req:
                if any(k in student_class or k in student_course for k in ["b.sc", "b.tech", "b.com", "ba", "ug", "undergraduate", "bca", "mbbs", "bba", "b.ed", "llb", "graduation"]):
                    is_edu_matched = True
            elif "postgraduate" in edu_req or "pg" in edu_req or "master" in edu_req:
                if any(k in student_class or k in student_course for k in ["m.sc", "m.tech", "m.com", "ma", "pg", "postgraduate", "mca", "mba", "md", "phd"]):
                    is_edu_matched = True
            elif "11-12" in edu_req or "higher secondary" in edu_req:
                if any(k in student_class for k in ["11", "12", "class 11", "class 12", "intermediate", "higher secondary"]):
                    is_edu_matched = True
            elif "9-10" in edu_req or "pre-matric" in edu_req:
                if any(k in student_class for k in ["9", "10", "class 9", "class 10"]):
                    is_edu_matched = True

            if is_edu_matched:
                positives.append(f"Academic Level matched: Relevant to your current program of study ({scholarship.education_level}).")
                score += 15
            elif student_class or student_course:
                warnings.append(f"Education level: Designed primarily for {scholarship.education_level} candidates.")
                score -= 10

        # 7. Disability Check
        disability_req = (scholarship.disability_requirement or "None").strip().lower()
        student_disability = bool(student_data.get("is_disabled") or student_data.get("has_disability"))
        if disability_req in ["mandatory", "pwd only", "disability only"]:
            if student_disability:
                positives.append("Divyangjan / PwD criteria: Specialized reservation for students with benchmark disability (40%+).")
                score += 25
            else:
                blockers.append("Reserved exclusively for Persons with Benchmark Disabilities (UDID card required).")
                score -= 50

        # Normalize score
        score = max(5, min(99, score))

        # Determine Final Categorical Status
        if blockers:
            status = "NOT_ELIGIBLE"
            score = min(score, 35)
            action = "Explore alternative national or state schemes matching your academic profile."
        elif warnings and score < 75:
            status = "PARTIALLY_MATCHED"
            action = "Update missing profile attributes or verify certificate eligibility before applying."
        elif warnings:
            status = "LIKELY_ELIGIBLE"
            action = "Review specific income and domicile documentation to ensure full compliance."
        else:
            status = "ELIGIBLE"
            score = max(score, 85)
            action = "Strong candidate. Assemble mandatory documents and initiate your application."

        # Document Checklist
        docs_needed = scholarship.parsed_documents

        return {
            "status": status,
            "fit_score": score,
            "positive_signals": positives,
            "warnings": warnings,
            "blockers": blockers,
            "documents_needed": docs_needed,
            "action_step": action
        }

    @classmethod
    def match_all(cls, scholarships, student_data: Dict[str, Any], limit: int = None) -> List[Dict[str, Any]]:
        """
        Evaluates a collection of scholarships against student attributes
        and ranks them by fit score and eligibility status.
        """
        results = []
        for s in scholarships:
            eval_res = cls.evaluate(s, student_data)
            results.append({
                "scholarship": s,
                "evaluation": eval_res,
                "fit_score": eval_res["fit_score"],
                "status": eval_res["status"]
            })

        # Sort: ELIGIBLE first, then LIKELY_ELIGIBLE, then PARTIALLY_MATCHED, then NOT_ELIGIBLE; then by score descending
        status_order = {"ELIGIBLE": 0, "LIKELY_ELIGIBLE": 1, "PARTIALLY_MATCHED": 2, "NOT_ELIGIBLE": 3}
        results.sort(key=lambda x: (status_order.get(x["status"], 4), -x["fit_score"]))

        if limit:
            return results[:limit]
        return results


eligibility_engine = ScholarshipEligibilityEngine()
evaluate_scholarship_eligibility = ScholarshipEligibilityEngine.evaluate
