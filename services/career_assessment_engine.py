"""
services/career_assessment_engine.py
==============================================================================
MPath Multi-Dimensional Career Discovery & Assessment Engine
==============================================================================
Deterministic, research-grounded evaluation engine that synthesizes:
- Holland's RIASEC vocational profile
- Work values, styles, and environmental fit
- Self-efficacy and cognitive persistence
- Academic feasibility, streams, and financial constraints
- Negative exclusions (deal-breakers) and trade-off detection
- Integration with MPath's 214+ Careers, 68 Courses, 1946 Colleges, 95 Exams,
  70 Scholarships, and 120 Internships.
"""

from typing import Dict, List, Any, Tuple
import json
import re
from sqlalchemy import or_, and_

from extensions import db
from models.career import Career
from models.career_course import CareerCourse
from models.career_exam import CareerExam
from models.course import Course, CollegeCourse
from models.college import College
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship
from services.career_assessment_questions import DISCOVERY_QUESTIONS, get_question_by_id


class CareerAssessmentEngine:
    """
    Core matching and counselling synthesis engine.
    """

    @classmethod
    def evaluate(cls, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point:
        1. Synthesizes multi-dimensional student profile.
        2. Evaluates all 214+ database careers.
        3. Identifies contradictions & trade-offs.
        4. Selects Top 5 Matches + 5-10 Adjacent Paths + 3-5 Lesser-Known Discoveries.
        5. Gathers relational ecosystem links (Courses, Colleges, Exams, Scholarships, Internships).
        6. Generates tailored counselling explanations & next 3 action experiments.
        """
        # Step 1: Synthesize student profile vector
        profile = cls._build_student_profile(form_data)

        # Step 2: Score all careers
        scored_careers = cls._score_all_careers(profile)

        # Step 3: Identify trade-offs & contradictions
        tradeoffs = cls._detect_contradictions_and_tradeoffs(profile, scored_careers)

        # Step 4: Stratify recommendations
        top_matches, adjacent_paths, unexpected_careers = cls._stratify_careers(
            scored_careers, profile
        )

        # Step 5: Enrich with ecosystem graph links & explainable counselling notes
        enriched_top = [cls._enrich_career_dossier(c_data, profile, "STRONG_MATCH") for c_data in top_matches]
        enriched_unexpected = [cls._enrich_career_dossier(c_data, profile, "UNEXPECTED_DISCOVERY") for c_data in unexpected_careers]
        enriched_adjacent = [cls._enrich_career_dossier(c_data, profile, "ADJACENT_PATH") for c_data in adjacent_paths]

        # Step 6: Generate action steps
        actions = cls._generate_action_steps(profile, enriched_top, enriched_unexpected)

        # Step 7: Headline summary
        dominant_style = profile.get("dominant_archetype", "Versatile Explorer")
        primary_match_title = enriched_top[0]["career"].title if enriched_top else "Career Discovery"
        primary_category = enriched_top[0]["career"].category if enriched_top else "Career Discovery"

        headline = f"Profile: {dominant_style} — Recommended Direction: {primary_category}"

        return {
            "version": "2.0.0",
            "recommended_category": primary_category,
            "headline": headline,
            "confidence_level": profile.get("confidence_level", "HIGH_CONFIDENCE"),
            "profile": profile,
            "tradeoffs": tradeoffs,
            "top_matches": enriched_top,
            "unexpected_careers": enriched_unexpected,
            "adjacent_paths": enriched_adjacent,
            "actions": actions,
            "total_evaluated": len(scored_careers)
        }

    # =========================================================================
    # 1. PROFILE SYNTHESIS
    # =========================================================================

    @classmethod
    def _build_student_profile(cls, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Construct multi-dimensional profile vector from form responses"""
        riasec = {"R": 0.0, "I": 0.0, "A": 0.0, "S": 0.0, "E": 0.0, "C": 0.0}
        work_values = {"security": 0.0, "income": 0.0, "impact": 0.0, "mastery": 0.0, "autonomy": 0.0, "stability": 0.0}
        environments = {"office": 0.0, "lab": 0.0, "field": 0.0, "studio": 0.0, "remote": 0.0}
        domain_affinities: Dict[str, float] = {}
        evidence_statements = []
        negative_dislikes = []

        self_efficacy_level = "moderate"
        study_tolerance = 3
        exam_tolerance = 3
        current_stream = "Any"
        current_level = "Undergraduate"
        need_scholarships = False
        earn_early = False
        math_discomfort = False

        # Iterate over question definitions and map selected keys
        for q in DISCOVERY_QUESTIONS:
            qid = q["id"]
            val = form_data.get(qid)
            if not val:
                continue

            if q.get("is_text"):
                # Handle open reflection text
                text_content = str(val).strip()
                if text_content:
                    extracted = cls._extract_keywords_from_text(text_content)
                    for dom, wt in extracted.items():
                        domain_affinities[dom] = domain_affinities.get(dom, 0.0) + wt
                continue

            # Multi-choice options match
            selected_option = None
            for opt in q.get("options", []):
                if opt["key"] == val or opt.get("label") == val:
                    selected_option = opt
                    break

            if not selected_option:
                continue

            # Record evidence
            if "evidence" in selected_option:
                evidence_statements.append({
                    "category": q.get("category"),
                    "text": selected_option["evidence"]
                })

            # RIASEC weights
            weights = selected_option.get("weights", {})
            for r_key in ["R", "I", "A", "S", "E", "C"]:
                if r_key in weights:
                    riasec[r_key] += weights[r_key]

            # Work values
            for v_key in ["security", "income", "impact", "mastery", "autonomy", "stability"]:
                full_v = f"value_{v_key}"
                if full_v in weights:
                    work_values[v_key] += weights[full_v]

            # Environments
            for env_key in ["office", "lab", "field", "studio", "remote"]:
                full_env = f"env_{env_key}"
                if full_env in weights:
                    environments[env_key] += weights[full_env]

            # Specific question behaviors
            if qid == "q3_self_efficacy":
                self_efficacy_level = selected_option.get("efficacy_level", "moderate")
                if selected_option.get("weights", {}).get("math_discomfort"):
                    math_discomfort = True

            elif qid == "q5_problem_type":
                dom = selected_option.get("domain_affinity")
                if dom:
                    domain_affinities[dom] = domain_affinities.get(dom, 0.0) + 4.0

            elif qid == "q8_study_investment_tolerance":
                study_tolerance = selected_option.get("weights", {}).get("study_tolerance", 3)
                if selected_option.get("weights", {}).get("earn_early"):
                    earn_early = True

            elif qid == "q9_exam_tolerance":
                exam_tolerance = selected_option.get("weights", {}).get("exam_tolerance", 3)

            elif qid == "q11_financial_constraints":
                if selected_option.get("weights", {}).get("need_scholarships"):
                    need_scholarships = True
                if selected_option.get("weights", {}).get("earn_early"):
                    earn_early = True

            elif qid == "q12_current_academic_level":
                current_stream = selected_option.get("stream", "Any")
                current_level = selected_option.get("level", "Undergraduate")

            elif qid == "q14_negative_preferences":
                dislike_key = selected_option.get("dislike")
                if dislike_key:
                    negative_dislikes.append({
                        "key": dislike_key,
                        "label": selected_option.get("label"),
                        "penalties": selected_option.get("penalty_clusters", [])
                    })

        # Normalize RIASEC vector
        total_r = sum(riasec.values()) or 1.0
        normalized_riasec = {k: round(v / total_r, 3) for k, v in riasec.items()}
        sorted_riasec = sorted(normalized_riasec.items(), key=lambda x: x[1], reverse=True)
        top_two_riasec = f"{sorted_riasec[0][0]}{sorted_riasec[1][0]}"

        # Derive natural language thinking archetype
        archetype_map = {
            "IR": "Investigative Builder (Technical & Scientific Problem-Solver)",
            "RI": "Realistic Thinker (Hands-On Engineer & Technologist)",
            "IA": "Curious Innovator (Analytical & Creative Synthesizer)",
            "AI": "Creative Strategist (Design & Conceptual Storyteller)",
            "IS": "Scientific Helper (Diagnostic, Health & Research Mind)",
            "SI": "Empathetic Analyst (Educator, Counselor & Societal Investigator)",
            "IE": "Strategic Thinker (Data-Driven Enterprise & Policy Architect)",
            "EI": "Enterprising Strategist (High-Impact Leader & Founder)",
            "IC": "Systematic Analyst (Precision Investigator & Quantitative Auditor)",
            "CI": "Structured Quantitative (Data Architect & Compliance Specialist)",
            "AS": "Expressive Facilitator (Arts, Media & Social Impact Creator)",
            "SA": "Humanistic Storyteller (Communications, Culture & People Advocate)",
            "SE": "Transformational Leader (Public Administration, Law & Social Mobilizer)",
            "ES": "Civic Entrepreneur (People-Centric Enterprise & Public Service)",
            "EC": "Commercial Director (Corporate Management, Finance & Scaling)",
            "CE": "Operational Organizer (Corporate Governance, Logistics & Finance)",
            "RC": "Technical Operator (High-Precision Systems & Infrastructure)",
            "CR": "Structured Technologist (Quality Engineering & Operations)",
            "RA": "Industrial Maker (Spatial Design, Architecture & Craft)",
            "AR": "Visual Fabricator (Creative Arts, Media & Spatial Designer)"
        }
        dominant_archetype = archetype_map.get(top_two_riasec, "Versatile Explorer (Multi-Disciplinary Aptitude)")

        return {
            "riasec_raw": riasec,
            "riasec_normalized": normalized_riasec,
            "top_riasec_code": top_two_riasec,
            "dominant_archetype": dominant_archetype,
            "work_values": work_values,
            "environments": environments,
            "domain_affinities": domain_affinities,
            "self_efficacy_level": self_efficacy_level,
            "math_discomfort": math_discomfort,
            "study_tolerance": study_tolerance,
            "exam_tolerance": exam_tolerance,
            "current_stream": current_stream,
            "current_level": current_level,
            "need_scholarships": need_scholarships,
            "earn_early": earn_early,
            "negative_dislikes": negative_dislikes,
            "evidence_statements": evidence_statements,
            "confidence_level": "HIGH_CONFIDENCE" if len(evidence_statements) >= 8 else "MODERATE_CONFIDENCE"
        }

    @classmethod
    def _extract_keywords_from_text(cls, text: str) -> Dict[str, float]:
        """Extract latent affinity signals from student's open reflection"""
        t = text.lower()
        signals = {}
        mappings = [
            (["code", "coding", "software", "program", "app", "web", "ai", "machine learning", "python"], "Technology & Computer Science", 2.0),
            (["biology", "medicine", "doctor", "health", "hospital", "patient", "clinical", "biotech"], "Healthcare & Medical Sciences", 2.0),
            (["money", "stock", "finance", "bank", "accounting", "invest", "crypto", "trading"], "Finance, Banking & Accounting", 2.0),
            (["design", "art", "draw", "video", "edit", "animation", "film", "creative", "ui"], "Design, Animation & Creative Arts", 2.0),
            (["nature", "forest", "wildlife", "animal", "plant", "farm", "agriculture", "climate", "environment"], "Agriculture, Food Technology & Environment", 2.0),
            (["law", "court", "justice", "debate", "constitution", "police", "civil service", "ias"], "Law & Legal Services", 2.0),
            (["robot", "mechanic", "engine", "circuit", "build", "drone", "hardware"], "Engineering & Manufacturing", 2.0),
            (["map", "geography", "gis", "space", "weather", "earth"], "Science, Research & Mathematics", 2.0),
            (["teach", "mentor", "child", "school", "explain", "counsel", "psychology"], "Education, Teaching & Academia", 2.0)
        ]
        for words, category, weight in mappings:
            if any(w in t for w in words):
                signals[category] = weight
        return signals

    # =========================================================================
    # 2. SCORING & MULTI-FACTOR EVALUATION
    # =========================================================================

    @classmethod
    def _score_all_careers(cls, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate all 214+ careers in the database against the student profile"""
        all_careers = Career.query.all()
        scored = []

        riasec = profile["riasec_normalized"]
        work_values = profile["work_values"]
        environments = profile["environments"]
        domain_affinities = profile["domain_affinities"]
        stream = profile["current_stream"]
        study_tol = profile["study_tolerance"]
        exam_tol = profile["exam_tolerance"]
        dislikes = profile["negative_dislikes"]
        math_discomfort = profile["math_discomfort"]

        for c in all_careers:
            # 1. RIASEC & Category Affinity (0 to 45 pts)
            affinity_score = cls._compute_category_affinity(c, riasec, domain_affinities)

            # 2. Work Values & Lifestyle Alignment (0 to 25 pts)
            values_score = cls._compute_values_alignment(c, work_values, environments)

            # 3. Academic Stream Feasibility (0 to 20 pts)
            feasibility_score, route_feasibility = cls._compute_stream_feasibility(c, stream)

            # 4. Self-Efficacy & Training Alignment (0 to 10 pts)
            efficacy_score = cls._compute_efficacy_alignment(c, study_tol, exam_tol, math_discomfort)

            # 5. Negative Preference Penalty
            penalty, penalty_reason = cls._compute_negative_penalty(c, dislikes)

            total_score = max(5.0, (affinity_score + values_score + feasibility_score + efficacy_score) - penalty)

            # Fit ratings for UI badges
            interest_fit = "HIGH" if affinity_score >= 28 else ("MEDIUM" if affinity_score >= 18 else "EXPLORATORY")
            values_fit = "HIGH" if values_score >= 16 else ("MEDIUM" if values_score >= 10 else "EXPLORATORY")
            feasibility_fit = "HIGH" if feasibility_score >= 15 else ("MEDIUM" if feasibility_score >= 10 else "ALTERNATIVE")

            scored.append({
                "career": c,
                "score": round(total_score, 1),
                "affinity_score": affinity_score,
                "values_score": values_score,
                "feasibility_score": feasibility_score,
                "efficacy_score": efficacy_score,
                "interest_fit": interest_fit,
                "values_fit": values_fit,
                "feasibility_fit": feasibility_fit,
                "route_feasibility": route_feasibility,
                "penalty_applied": penalty > 0,
                "penalty_reason": penalty_reason,
                "is_lesser_known": bool(c.is_lesser_known)
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    @classmethod
    def _compute_category_affinity(cls, c: Career, riasec: Dict[str, float], domain_affinities: Dict[str, float]) -> float:
        """Calculate interest congruence between career and RIASEC profile"""
        cat = c.category or ""
        sub = c.sub_category or ""
        title = c.title or ""
        clusters = (c.interest_clusters or "").lower()

        score = 10.0

        # RIASEC category heuristic
        if "Technology" in cat or "Computer" in cat:
            score += (riasec.get("I", 0.0) * 20.0) + (riasec.get("R", 0.0) * 12.0)
        elif "Healthcare" in cat or "Medical" in cat:
            score += (riasec.get("I", 0.0) * 18.0) + (riasec.get("S", 0.0) * 16.0)
        elif "Engineering" in cat or "Manufacturing" in cat:
            score += (riasec.get("R", 0.0) * 22.0) + (riasec.get("I", 0.0) * 12.0)
        elif "Design" in cat or "Creative" in cat or "Media" in cat:
            score += (riasec.get("A", 0.0) * 26.0) + (riasec.get("E", 0.0) * 8.0)
        elif "Finance" in cat or "Accounting" in cat or "Banking" in cat:
            score += (riasec.get("C", 0.0) * 22.0) + (riasec.get("E", 0.0) * 12.0)
        elif "Government" in cat or "Civil Services" in cat or "Defence" in cat:
            score += (riasec.get("E", 0.0) * 15.0) + (riasec.get("C", 0.0) * 14.0) + (riasec.get("S", 0.0) * 8.0)
        elif "Law" in cat or "Legal" in cat:
            score += (riasec.get("E", 0.0) * 16.0) + (riasec.get("I", 0.0) * 12.0) + (riasec.get("S", 0.0) * 8.0)
        elif "Agriculture" in cat or "Environment" in cat:
            score += (riasec.get("R", 0.0) * 18.0) + (riasec.get("I", 0.0) * 14.0)
        elif "Education" in cat or "Teaching" in cat:
            score += (riasec.get("S", 0.0) * 24.0) + (riasec.get("I", 0.0) * 10.0)
        elif "Business" in cat or "Management" in cat:
            score += (riasec.get("E", 0.0) * 22.0) + (riasec.get("C", 0.0) * 10.0)
        elif "Science" in cat or "Research" in cat:
            score += (riasec.get("I", 0.0) * 26.0) + (riasec.get("R", 0.0) * 8.0)
        elif "Aviation" in cat or "Logistics" in cat:
            score += (riasec.get("R", 0.0) * 15.0) + (riasec.get("C", 0.0) * 15.0)
        else:
            score += 15.0 * (riasec.get("I", 0.0) + riasec.get("E", 0.0))

        # Direct domain boost from problem-type choices or open text
        for dom, boost in domain_affinities.items():
            if dom.lower() in cat.lower() or cat.lower() in dom.lower():
                score += boost * 2.5

        return min(45.0, score)

    @classmethod
    def _compute_values_alignment(cls, c: Career, values: Dict[str, float], envs: Dict[str, float]) -> float:
        """Calculate match between student's values/environment and career attributes"""
        score = 8.0
        cat = (c.category or "").lower()
        work_env = (c.work_environment or "").lower()
        work_modes = (c.work_modes or "").lower()
        govt_opps = bool(c.government_opportunities)

        # Government / Stability values
        if values.get("stability", 0.0) > 2.0 or values.get("security", 0.0) > 2.0:
            if "government" in cat or govt_opps or "defence" in cat:
                score += 7.0
            elif "banking" in cat or "teaching" in cat:
                score += 4.0

        # Impact value
        if values.get("impact", 0.0) > 2.0:
            if any(k in cat for k in ["healthcare", "medical", "education", "social", "law", "environment"]):
                score += 7.0

        # Autonomy / Creative freedom
        if values.get("autonomy", 0.0) > 2.0:
            if any(k in cat for k in ["design", "creative", "media", "consulting", "technology"]):
                score += 5.0
            if "remote" in work_modes:
                score += 3.0

        # Environmental alignment
        if envs.get("lab", 0.0) > 2.0 and ("hospital" in work_env or "lab" in work_env):
            score += 5.0
        if envs.get("field", 0.0) > 2.0 and ("field" in work_env or "outdoor" in work_env or "site" in work_env):
            score += 5.0
        if envs.get("office", 0.0) > 2.0 and "office" in work_env:
            score += 4.0
        if envs.get("remote", 0.0) > 2.0 and ("remote" in work_modes or "hybrid" in work_modes):
            score += 4.0

        return min(25.0, score)

    @classmethod
    def _compute_stream_feasibility(cls, c: Career, stream: str) -> Tuple[float, str]:
        """Check education eligibility and alternative pathway accessibility"""
        pref = (c.preferred_streams or "").lower()
        min_qual = (c.minimum_qualification or "").lower()

        if not pref or "any" in pref:
            return 20.0, "DIRECT_ENTRY (Any stream eligible)"

        s_clean = stream.lower()
        if "pcm" in s_clean and ("pcm" in pref or "science" in pref):
            return 20.0, "DIRECT_ENTRY (Science PCM aligns directly)"
        if "pcb" in s_clean and ("pcb" in pref or "science" in pref):
            return 20.0, "DIRECT_ENTRY (Science PCB aligns directly)"
        if "commerce" in s_clean and "commerce" in pref:
            return 20.0, "DIRECT_ENTRY (Commerce stream aligns directly)"
        if "arts" in s_clean and ("arts" in pref or "humanities" in pref):
            return 20.0, "DIRECT_ENTRY (Arts/Humanities aligns directly)"
        if "diploma" in s_clean and ("diploma" in pref or "vocational" in pref):
            return 20.0, "DIRECT_ENTRY (Diploma/Vocational bridge ready)"

        # Alternative bridge routes
        if "class 10" in s_clean:
            return 18.0, "STREAM_EXPLORATION (Selection step ahead in Class 11)"

        # Interdisciplinary bridges
        if "pcm" in s_clean and any(k in pref for k in ["commerce", "arts"]):
            return 18.0, "ALTERNATIVE_BRIDGE (Science students can transition)"
        if "commerce" in s_clean and "arts" in pref:
            return 17.0, "ALTERNATIVE_BRIDGE (Commerce to Arts/Law/Design transition)"
        if "arts" in s_clean and any(k in pref for k in ["pcm", "pcb", "medical"]):
            return 7.0, "RESTRICTED (Requires science bridge or non-clinical pathway)"

        return 12.0, "ALTERNATIVE_ROUTE (Accessible via entrance test or diploma)"

    @classmethod
    def _compute_efficacy_alignment(cls, c: Career, study_tol: int, exam_tol: int, math_discomfort: bool) -> float:
        """Verify training stamina and subject comfort"""
        score = 8.0
        cat = (c.category or "").lower()
        title = (c.title or "").lower()
        skills = ((c.technical_skills or "") + " " + (c.skills_required or "")).lower()

        # Math discomfort check
        if math_discomfort and ("data science" in title or "actuary" in title or "algorithm" in skills):
            score -= 5.0

        # Long study tolerance vs medical/research
        if study_tol < 3 and ("doctor" in title or "surgeon" in title or "research scientist" in title):
            score -= 4.0
        elif study_tol >= 4 and ("doctor" in title or "research" in title or "lawyer" in title):
            score += 2.0

        # Competitive exam tolerance vs civil services
        if exam_tol < 3 and ("civil services" in cat or "ias" in title or "ips" in title):
            score -= 4.0
        elif exam_tol >= 4 and ("civil services" in cat or "defence" in cat):
            score += 2.0

        return max(1.0, min(10.0, score))

    @classmethod
    def _compute_negative_penalty(cls, c: Career, dislikes: List[Dict[str, Any]]) -> Tuple[float, str]:
        """Apply soft or hard penalties if career clashes with student's deal-breakers"""
        total_penalty = 0.0
        reasons = []

        cat = (c.category or "").lower()
        title = (c.title or "").lower()
        work_env = (c.work_environment or "").lower()

        for d in dislikes:
            key = d["key"]
            if key == "repetitive_desk_work":
                if any(k in title for k in ["data entry", "clerk", "bookkeeper", "tax assistant"]):
                    total_penalty += 25.0
                    reasons.append("Conflicts with dislike for repetitive isolated desk work")
            elif key == "aggressive_sales":
                if any(k in title for k in ["sales", "business development", "telemarketing", "broker"]):
                    total_penalty += 25.0
                    reasons.append("Conflicts with dislike for commercial sales quotas")
            elif key == "clinical_medical":
                if any(k in title for k in ["doctor", "surgeon", "dentist", "nurse", "paramedic", "trauma"]):
                    total_penalty += 35.0
                    reasons.append("Conflicts with dislike for clinical surgery and hospital emergencies")
            elif key == "strenuous_outdoor":
                if "outdoor" in work_env or any(k in title for k in ["mining", "field construction", "surveyor", "drilling"]):
                    total_penalty += 20.0
                    reasons.append("Conflicts with preference against harsh outdoor physical labor")
            elif key == "constant_public_conflict":
                if any(k in title for k in ["litigation", "criminal lawyer", "anchor", "court advocate"]):
                    total_penalty += 20.0
                    reasons.append("Conflicts with preference against contentious public confrontation")
            elif key == "unpredictable_income":
                if any(k in title for k in ["freelance", "founder", "commission agent", "independent artist"]):
                    total_penalty += 15.0
                    reasons.append("Conflicts with strong need for predictable monthly compensation")

        return total_penalty, "; ".join(reasons) if reasons else ""

    # =========================================================================
    # 3. CONTRADICTIONS & TRADE-OFFS
    # =========================================================================

    @classmethod
    def _detect_contradictions_and_tradeoffs(cls, profile: Dict[str, Any], scored_careers: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Identify constructive dissonance in student's choices and suggest bridges"""
        tradeoffs = []

        study_tol = profile.get("study_tolerance", 3)
        exam_tol = profile.get("exam_tolerance", 3)
        math_discomfort = profile.get("math_discomfort", False)
        earn_early = profile.get("earn_early", False)
        stream = profile.get("current_stream", "")

        # Contradiction 1: High Healthcare interest vs. Low study endurance
        bio_affinity = profile.get("domain_affinities", {}).get("Healthcare & Medical Sciences", 0.0)
        if (bio_affinity >= 3.0 or "PCB" in stream) and study_tol <= 2:
            tradeoffs.append({
                "type": "EDUCATION_DURATION",
                "title": "Healthcare Passion vs. Training Duration",
                "observation": "You show strong attraction to healthcare and helping others, but you indicated a preference for a shorter training duration (1-3 years).",
                "guidance": "Traditional MBBS requires 5.5 to 8+ years. Consider Allied Health Sciences (B.Sc Medical Lab Technology, Radiology, Perfusion Tech, or Optometry) which allow you to work directly in healthcare settings within 3-4 years.",
                "alternative_avenues": "Medical Lab Scientist, Clinical Data Coordinator, Radiologic Technologist, Optometrist"
            })

        # Contradiction 2: High Civil Services/Govt vs. Low competitive exam tolerance
        govt_affinity = profile.get("domain_affinities", {}).get("Government, Defence & Civil Services", 0.0)
        if govt_affinity >= 3.0 and exam_tol <= 2:
            tradeoffs.append({
                "type": "EXAM_COMPETITION",
                "title": "Public Impact vs. Competitive Exam Risk",
                "observation": "You are drawn to civic authority and societal governance, but you prefer skill/interview evaluations over multi-year competitive exam grinds.",
                "guidance": "UPSC CSE has an acceptance rate below 0.2%. You can achieve profound societal impact with higher certainty through Public Policy degrees, State Social Welfare research, NGO Program Leadership, or Corporate CSR management.",
                "alternative_avenues": "Public Policy Analyst, Development Sector Program Manager, Think Tank Researcher"
            })

        # Contradiction 3: Tech & Automation Interest vs. Math Discomfort
        tech_affinity = profile.get("domain_affinities", {}).get("Technology & Computer Science", 0.0)
        if tech_affinity >= 3.0 and math_discomfort:
            tradeoffs.append({
                "type": "SKILL_ALIGNMENT",
                "title": "Technology Affinity vs. Quantitative Friction",
                "observation": "You are eager to work in technology and digital systems, but you find heavy formulaic mathematics intimidating.",
                "guidance": "Software engineering and AI rely heavily on discrete math and linear algebra. However, tech contains enormous high-paying avenues that emphasize user psychology, visual systems, and structured communication rather than calculus.",
                "alternative_avenues": "UI/UX Product Designer, Technical Writer, Product Operations Manager, IT Business Analyst"
            })

        # Contradiction 4: Urgent Early Earning vs. High-Tuition Degree
        if earn_early and profile.get("need_scholarships", False):
            tradeoffs.append({
                "type": "FINANCIAL_FEASIBILITY",
                "title": "Early Income Urgency & Fee Management",
                "observation": "You indicated a need to start earning within 2-3 years to support your family while managing education costs.",
                "guidance": "Prioritize polytechnic diplomas with lateral entry schemes, government ITIs, or university programs with mandatory paid apprenticeships (like B.Voc or corporate sponsored internships).",
                "alternative_avenues": "Polytechnic Engineering Diplomas, AICTE Paid Apprenticeships, Vocational Certifications"
            })

        return tradeoffs

    # =========================================================================
    # 4. STRATIFIED DISCOVERY
    # =========================================================================

    @classmethod
    def _stratify_careers(cls, scored_careers: List[Dict[str, Any]], profile: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Partition careers into:
        - Top 5 Strong Matches
        - 3-5 'You May Not Have Considered' (Lesser known careers)
        - 5-10 Adjacent / Alternative Pathways
        """
        # Filter out heavy penalty disqualifications
        valid_candidates = [c for c in scored_careers if not c.get("penalty_applied") or c["score"] >= 40.0]

        top_matches = []
        unexpected = []
        adjacent = []

        seen_ids = set()

        # 1. Select Top 5 Strong Matches (Ensure category diversity: max 2 from same category in top 5)
        cat_counts: Dict[str, int] = {}
        for item in valid_candidates:
            c = item["career"]
            cat = c.category or "General"
            if cat_counts.get(cat, 0) < 2 and c.id not in seen_ids:
                top_matches.append(item)
                seen_ids.add(c.id)
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
                if len(top_matches) == 5:
                    break

        # Fallback if strict category limit restricted matches
        if len(top_matches) < 5:
            for item in valid_candidates:
                c = item["career"]
                if c.id not in seen_ids:
                    top_matches.append(item)
                    seen_ids.add(c.id)
                    if len(top_matches) == 5:
                        break

        # 2. Select 3-5 "You May Not Have Considered" (Prioritize is_lesser_known == True with score >= 35)
        lesser_known_pool = [c for c in valid_candidates if c["career"].is_lesser_known and c["career"].id not in seen_ids]
        for item in lesser_known_pool[:4]:
            unexpected.append(item)
            seen_ids.add(item["career"].id)

        # Fallback for unexpected if not enough flagged lesser_known
        if len(unexpected) < 3:
            for item in valid_candidates:
                c = item["career"]
                # Look for niche keywords in title or sub_category
                niche_keywords = ["analyst", "informatics", "cartographer", "actuarial", "auditor", "specialist", "counsellor", "technologist"]
                if c.id not in seen_ids and any(k in (c.title or "").lower() for k in niche_keywords):
                    unexpected.append(item)
                    seen_ids.add(c.id)
                    if len(unexpected) >= 3:
                        break

        # 3. Select 5-8 Adjacent Alternatives across diverse sectors
        for item in valid_candidates:
            c = item["career"]
            if c.id not in seen_ids:
                adjacent.append(item)
                seen_ids.add(c.id)
                if len(adjacent) >= 7:
                    break

        return top_matches, adjacent, unexpected

    # =========================================================================
    # 5. ECOSYSTEM GRAPH ENRICHMENT
    # =========================================================================

    @classmethod
    def _enrich_career_dossier(cls, c_data: Dict[str, Any], profile: Dict[str, Any], match_tier: str) -> Dict[str, Any]:
        """
        Pull actual relational records from MPath database:
        Career -> CareerCourse -> Course -> CollegeCourse -> College
        Career -> CareerExam -> GovernmentExam
        Career -> Scholarships
        Career -> Internships
        """
        career: Career = c_data["career"]

        # 1. Relational Courses
        career_courses = (
            CareerCourse.query.filter_by(career_id=career.id)
            .order_by(CareerCourse.relationship_type.asc())
            .all()
        )
        course_ids = [cc.course_id for cc in career_courses]
        linked_courses = Course.query.filter(Course.id.in_(course_ids)).all() if course_ids else []

        # 2. Linked Colleges (traversed through CollegeCourse for those courses)
        linked_colleges = []
        if course_ids:
            college_courses = (
                CollegeCourse.query.filter(CollegeCourse.course_id.in_(course_ids))
                .limit(6)
                .all()
            )
            col_ids = [cc.college_id for cc in college_courses]
            if col_ids:
                linked_colleges = College.query.filter(College.id.in_(col_ids)).limit(4).all()

        # Fallback to general colleges if no relational course link
        if not linked_colleges:
            linked_colleges = College.query.order_by(College.rating.desc() if hasattr(College, "rating") else College.id.asc()).limit(3).all()

        # 3. Relational Government & Entrance Exams
        career_exams = (
            CareerExam.query.filter_by(career_id=career.id)
            .order_by(CareerExam.importance.asc())
            .all()
        )
        exam_ids = [ce.exam_id for ce in career_exams]
        linked_exams = GovernmentExam.query.filter(GovernmentExam.id.in_(exam_ids)).all() if exam_ids else []

        # Fallback if no direct exam mapping exists
        if not linked_exams and career.category:
            cat_keyword = career.category.split(",")[0].split("&")[0].strip()
            linked_exams = GovernmentExam.query.filter(GovernmentExam.category.ilike(f"%{cat_keyword}%")).limit(2).all()

        # 4. Relevant Scholarships
        linked_scholarships = []
        stream = profile.get("current_stream", "")
        cat_search = career.category.split("&")[0].strip() if career.category else ""
        scholarship_query = Scholarship.query.filter(
            or_(
                Scholarship.category.ilike(f"%{cat_search}%"),
                Scholarship.streams.ilike(f"%{stream}%") if stream else False,
                Scholarship.category.ilike("%Merit%")
            )
        ).limit(3).all()
        linked_scholarships = scholarship_query

        # 5. Matching Internships
        linked_internships = []
        cat_keywords = [w for w in career.title.split() if len(w) > 3]
        if cat_keywords:
            internship_filters = [Internship.title.ilike(f"%{kw}%") for kw in cat_keywords[:2]]
            if career.industry:
                internship_filters.append(Internship.domain.ilike(f"%{career.industry}%"))
            linked_internships = Internship.query.filter(or_(*internship_filters)).limit(3).all()

        if not linked_internships:
            linked_internships = Internship.query.order_by(Internship.id.desc()).limit(2).all()

        # 6. Generate tailored counselling narrative
        counselling_why = cls._generate_tailored_why_explanation(career, profile, c_data)
        potential_challenge = cls._generate_tailored_challenge(career, profile)

        # 7. Parsed entry routes
        entry_routes = career.parsed_entry_routes
        if not entry_routes:
            entry_routes = [
                {"title": "Standard University Route", "description": f"Pursue a recognized undergraduate degree aligned with {career.title}, build internship credentials, and enter entry-level roles."},
                {"title": "Skill-First / Diploma Route", "description": f"Complete specialized technical diplomas or certifications and transition via junior apprenticeship roles."}
            ]

        return {
            "career": career,
            "match_tier": match_tier,
            "score": c_data["score"],
            "interest_fit": c_data["interest_fit"],
            "values_fit": c_data["values_fit"],
            "feasibility_fit": c_data["feasibility_fit"],
            "route_feasibility": c_data["route_feasibility"],
            "counselling_why": counselling_why,
            "potential_challenge": potential_challenge,
            "entry_routes": entry_routes,
            "linked_courses": linked_courses,
            "linked_colleges": linked_colleges,
            "linked_exams": linked_exams,
            "linked_scholarships": linked_scholarships,
            "linked_internships": linked_internships,
            "reality_check": career.reality_check_points,
            "next_steps": career.parsed_next_steps
        }

    @classmethod
    def _generate_tailored_why_explanation(cls, career: Career, profile: Dict[str, Any], c_data: Dict[str, Any]) -> str:
        """Construct evidence-grounded counselling reasoning referencing student responses"""
        reasons = []
        riasec = profile["riasec_normalized"]
        top_code = profile["top_riasec_code"]
        values = profile["work_values"]

        if "I" in top_code and ("Technology" in career.category or "Science" in career.category or "Medical" in career.category):
            reasons.append("Your responses showed strong investigative curiosity and patience with deep analytical problem-solving.")

        if "R" in top_code and ("Engineering" in career.category or "Agriculture" in career.category or "Aviation" in career.category):
            reasons.append("You indicated high engagement when building, repairing, and experimenting with physical or tangible systems.")

        if "A" in top_code and ("Design" in career.category or "Media" in career.category or "Creative" in career.category):
            reasons.append("Your profile highlights a natural instinct for visual communication, narrative framing, and creative aesthetics.")

        if "S" in top_code and ("Education" in career.category or "Healthcare" in career.category or "Social" in career.category):
            reasons.append("You derive genuine energy from human empathy, mentoring, and directly improving people's lives.")

        if "E" in top_code and ("Business" in career.category or "Government" in career.category or "Law" in career.category):
            reasons.append("You showed a natural comfort with mobilizing teams, commercial negotiation, and leadership responsibility.")

        if "C" in top_code and ("Finance" in career.category or "Accounting" in career.category or "Logistics" in career.category):
            reasons.append("You demonstrated high appreciation for structured order, precision verification, and financial systems.")

        if values.get("security", 0.0) >= 3.0 and career.government_opportunities:
            reasons.append("This avenue directly satisfies your value for institutional longevity and structured job security.")

        if values.get("impact", 0.0) >= 3.0:
            reasons.append("This role provides clear, tangible social contribution that aligns with your core work values.")

        if not reasons:
            reasons.append(f"Your multi-dimensional cognitive profile and stated lifestyle preferences align strongly with the day-to-day demands of {career.title}.")

        return " ".join(reasons)

    @classmethod
    def _generate_tailored_challenge(cls, career: Career, profile: Dict[str, Any]) -> str:
        """Formulate constructive trade-offs for this specific career"""
        points = career.reality_check_points
        if points:
            return points[0]
        cat = (career.category or "").lower()
        if "government" in cat:
            return "Requires disciplined long-term competitive preparation with realistic backup planning."
        elif "medical" in cat:
            return "Demands extensive training duration and emotional resilience in high-pressure clinical situations."
        elif "design" in cat or "creative" in cat:
            return "Requires consistent self-directed portfolio creation and adaptation to evolving software tools."
        elif "technology" in cat:
            return "Requires continuous upskilling and willingness to debug complex logic independently."
        return "Demands continuous skill refinement and proactive internship networking to secure top placements."

    # =========================================================================
    # 6. ACTION STEPS SYNTHESIS
    # =========================================================================

    @classmethod
    def _generate_action_steps(cls, profile: Dict[str, Any], top_matches: List[Dict[str, Any]], unexpected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Construct the 'Your Next 3 Actions' real-world micro-experiments"""
        actions = []

        career_1 = top_matches[0]["career"] if top_matches else None
        career_2 = top_matches[1]["career"] if len(top_matches) > 1 else None
        unexpected_1 = unexpected[0]["career"] if unexpected else None

        # Action 1: Comparative Exploration
        c1_title = career_1.title if career_1 else "Target Career"
        c2_title = career_2.title if career_2 else "Alternative Route"
        actions.append({
            "step": 1,
            "title": f"Compare {c1_title} vs. {c2_title} Dossiers",
            "description": f"Read the full MPath career dossiers for both {c1_title} and {c2_title}. Check their daily work environments, salary brackets, and required entrance exams.",
            "link_type": "CAREER_DETAIL",
            "link_slug": career_1.slug if career_1 else "career-discovery"
        })

        # Action 2: Pathway & College Verification
        actions.append({
            "step": 2,
            "title": "Inspect Approved Degrees & Verified Colleges",
            "description": f"Examine the canonical degree routes linked to {c1_title} in MPath and view the list of 1,946 verified colleges to understand fee structures and admission cutoffs.",
            "link_type": "COLLEGE_DISCOVERY",
            "link_url": "/colleges/"
        })

        # Action 3: One-Week Low-Stakes Real-World Experiment
        exp_text = cls._generate_experiment_for_career(career_1)
        actions.append({
            "step": 3,
            "title": "Complete a 7-Day Low-Stakes Micro-Experiment",
            "description": exp_text,
            "link_type": "EXPERIMENT",
            "link_url": None
        })

        return actions

    @classmethod
    def _generate_experiment_for_career(cls, career: Career) -> str:
        """Design an actionable real-world micro-experiment to test interest before committing"""
        cat = (career.category or "").lower() if career else ""
        title = (career.title or "").lower() if career else ""

        if "technology" in cat or "software" in title or "data" in title:
            return "Build a tiny functional project: follow a free 4-hour Python or web tutorial to create an interactive calculator or data dashboard. Observe if debugging keeps you curious or drains you."
        elif "medical" in cat or "healthcare" in cat:
            return "Shadow a day in healthcare: read two genuine medical case studies or interview a local pharmacist/allied health professional about their day-to-day shifts and statutory registration."
        elif "design" in cat or "creative" in cat:
            return "Design a real-world redesign: pick an app or physical poster that bothers you, create three alternative design drafts, and show them to 3 people for constructive critique."
        elif "law" in cat:
            return "Analyze a legal dilemma: read a recent public High Court or Supreme Court judgment summary, write a 1-page summary of both sides' legal arguments, and see if the reasoning excites you."
        elif "finance" in cat or "accounting" in cat:
            return "Perform a balance sheet audit: download the annual financial report of a public Indian company (e.g. Tata Motors or Infosys) and identify their top three revenue sources and expense drivers."
        elif "government" in cat or "civil" in cat:
            return "Solve a civic problem: identify a public infrastructure or governance breakdown in your local neighborhood and draft an official 2-page administrative proposal detailing budget and execution."
        elif "agriculture" in cat or "environment" in cat:
            return "Conduct an ecological audit: investigate local water testing data or interview a local farming cooperative about seed pricing and climate challenges in your region."
        else:
            return f"Spend 3 hours researching the day-to-day life of a working {career.title if career else 'professional'}, read an industry interview, and list 3 skills you would be excited to learn."
