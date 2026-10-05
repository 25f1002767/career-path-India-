from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from extensions import db
from models.user import User
from models.career import Career
from models.college import College
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship
from models.assessment import AssessmentResult
from models.resume import Resume
from models.saved_career import SavedCareer
from models.saved_college import SavedCollege
from models.saved_opportunity import SavedOpportunity
from models.student_profile import StudentProfile
from models.roadmap import CareerRoadmap
from services.career_match_engine import calculate_match_score

dashboard = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(session["user_id"])
    profile = StudentProfile.query.filter_by(user_id=user.id).first()

    # Profile completion calculation
    profile_fields = [
        getattr(user, "contact_number", None),
        getattr(user, "class_grade", None),
        getattr(user, "stream", None),
        getattr(user, "college_name", None),
        getattr(user, "state", None),
        profile.career_goal if profile else None,
        profile.interests if profile else None,
        profile.strengths if profile else None,
        profile.learning_style if profile else None,
    ]
    completed_count = sum(1 for f in profile_fields if f and str(f).strip())
    profile_completion = int((completed_count / len(profile_fields)) * 100)

    # Latest Assessment
    assessment = AssessmentResult.query.filter_by(
        user_id=user.id
    ).order_by(
        AssessmentResult.id.desc()
    ).first()

    # Latest Resume
    resume = Resume.query.filter_by(
        user_id=user.id
    ).order_by(
        Resume.created_at.desc()
    ).first()

    # Saved items
    saved_careers = SavedCareer.query.filter_by(user_id=user.id).all()
    saved_colleges = SavedCollege.query.filter_by(user_id=user.id).all()
    saved_opportunities = SavedOpportunity.query.filter_by(user_id=user.id).all()

    # Dynamic Explainable Career Recommendations
    # Build student context
    student_ctx = {
        "stream": getattr(user, "stream", "") or "",
        "class_grade": getattr(user, "class_grade", "") or "",
        "career_interest": getattr(user, "career_interest", "") or "",
        "interests": profile.interests if profile else "",
        "strengths": profile.strengths if profile else "",
        "recommended_category": assessment.recommended_category if assessment else ""
    }

    all_careers = Career.query.all()
    career_matches = []

    for c in all_careers:
        score, reasons = calculate_match_score(student_ctx, c)
        career_matches.append({
            "career": c,
            "score": score,
            "reasons": reasons
        })

    career_matches.sort(key=lambda x: x["score"], reverse=True)
    top_career_matches = career_matches[:4]

    # Target Career Roadmap (Top recommended or first saved)
    target_career = None
    target_roadmap = None

    if saved_careers:
        target_career = saved_careers[0].career
    elif top_career_matches:
        target_career = top_career_matches[0]["career"]

    if target_career:
        target_roadmap = CareerRoadmap.query.filter_by(career_id=target_career.id).first()

    # Featured verified opportunities from database
    upcoming_exams = GovernmentExam.query.limit(3).all()
    featured_scholarships = Scholarship.query.limit(3).all()
    featured_internships = Internship.query.limit(3).all()

    return render_template(
        "dashboard/index.html",
        user=user,
        profile=profile,
        profile_completion=profile_completion,
        assessment=assessment,
        resume=resume,
        saved_careers=saved_careers,
        saved_colleges=saved_colleges,
        saved_opportunities=saved_opportunities,
        top_career_matches=top_career_matches,
        target_career=target_career,
        target_roadmap=target_roadmap,
        upcoming_exams=upcoming_exams,
        featured_scholarships=featured_scholarships,
        featured_internships=featured_internships
    )