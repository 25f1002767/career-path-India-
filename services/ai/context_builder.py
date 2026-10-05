import json
from typing import Dict, Any, Optional
from models.user import User
from models.student_profile import StudentProfile
from models.assessment import AssessmentResult
from models.saved_career import SavedCareer
from models.saved_college import SavedCollege
from models.scholarship import ScholarshipApplication
from models.resume import Resume
from services.ai.memory_manager import MemoryManager


def build_student_context(user_id: Optional[int], session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Assembles a comprehensive, structured student context dossier
    combining academic profile, smart assessment signals, saved opportunities,
    and long-term conversational memory.
    """
    context = {
        "is_authenticated": bool(user_id),
        "name": "Student",
        "class_grade": "",
        "stream": "",
        "school_or_college": "",
        "career_goal": "",
        "interests": "",
        "strengths": "",
        "saved_careers": [],
        "saved_colleges": [],
        "assessment": None,
        "memories": [],
        "has_completed_assessment": False
    }

    # Fetch long-term memories
    context["memories"] = MemoryManager.get_memories_summary(user_id, session_id)

    if not user_id:
        return context

    user = User.query.get(user_id)
    if not user:
        return context

    context["name"] = user.full_name or "Student"
    context["email"] = user.email or ""
    context["class_grade"] = getattr(user, "class_grade", "") or ""
    context["stream"] = getattr(user, "stream", "") or ""
    context["school_or_college"] = getattr(user, "college_name", "") or ""
    context["course"] = getattr(user, "course", "") or ""
    context["career_goal"] = getattr(user, "career_interest", "") or ""

    # Student Profile
    profile = StudentProfile.query.filter_by(user_id=user.id).first()
    if profile:
        context["interests"] = profile.interests or context["interests"]
        context["strengths"] = profile.strengths or context["strengths"]
        context["career_goal"] = profile.career_goal or context["career_goal"]
        if not context["class_grade"] and profile.current_class:
            context["class_grade"] = profile.current_class
        if not context["school_or_college"] and profile.school_college:
            context["school_or_college"] = profile.school_college

    # Smart Assessment Signals
    latest_assessment = (
        AssessmentResult.query.filter_by(user_id=user.id)
        .order_by(AssessmentResult.id.desc())
        .first()
    )

    if latest_assessment:
        context["has_completed_assessment"] = True
        assessment_summary = {
            "recommended_category": latest_assessment.recommended_category,
            "headline": latest_assessment.summary_headline,
            "confidence_level": latest_assessment.confidence_level
        }

        # Parse profile_json if present (from Smart Assessment)
        if latest_assessment.profile_json:
            try:
                pj = json.loads(latest_assessment.profile_json)
                assessment_summary.update({
                    "riasec_code": pj.get("top_riasec_code"),
                    "archetype": pj.get("dominant_archetype"),
                    "work_values": pj.get("work_values"),
                    "environments": pj.get("environments"),
                    "math_discomfort": pj.get("math_discomfort", False),
                    "study_tolerance": pj.get("study_tolerance"),
                    "exam_tolerance": pj.get("exam_tolerance"),
                    "stream": pj.get("current_stream"),
                    "deal_breakers": [d.get("label") for d in pj.get("negative_dislikes", []) if isinstance(d, dict)]
                })
                if pj.get("current_stream") and not context["stream"]:
                    context["stream"] = pj.get("current_stream")
            except Exception:
                pass

        context["assessment"] = assessment_summary

    # Saved Careers
    saved_c = SavedCareer.query.filter_by(user_id=user.id).all()
    context["saved_careers"] = [s.career.title for s in saved_c if s.career]

    # Saved Colleges
    saved_cols = SavedCollege.query.filter_by(user_id=user.id).all()
    context["saved_colleges"] = [s.college.name for s in saved_cols if s.college]

    return context