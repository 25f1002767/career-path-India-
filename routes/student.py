from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request
)

from extensions import db

from models.user import User
from models.resume import Resume
from models.career import Career
from models.saved_career import SavedCareer
from models.assessment import AssessmentResult
from models.career_match import CareerMatch
from models.internship import Internship
from models.scholarship import Scholarship
from models.exam import GovernmentExam
from models.learning_progress import LearningProgress
from models.roadmap import CareerRoadmap
from models.student_profile import StudentProfile

from services.ai_recommendation import AIRecommendationService

student = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


# ==========================================
# Student Dashboard
# ==========================================

@student.route("/dashboard")
def dashboard():

    # --------------------------------------
    # Login Check
    # --------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    # --------------------------------------
    # Current User
    # --------------------------------------

    user = User.query.get(user_id)

    # --------------------------------------
    # Assessment History
    # --------------------------------------

    assessments = AssessmentResult.query.filter_by(
        user_id=user_id
    ).order_by(
        AssessmentResult.created_at.desc()
    ).all()

    history = assessments

    # --------------------------------------
    # Latest Assessment
    # --------------------------------------

    latest = None

    if assessments:

        latest = assessments[0]

    # --------------------------------------
    # Career Matches
    # --------------------------------------

    matches = CareerMatch.query.filter_by(
        user_id=user_id
    ).order_by(
        CareerMatch.match_percentage.desc()
    ).all()

    # --------------------------------------
    # Saved Careers
    # --------------------------------------

    saved = SavedCareer.query.filter_by(
        user_id=user_id
    ).all()

    # --------------------------------------
    # Latest Resume
    # --------------------------------------

    resume = Resume.query.filter_by(
        user_id=user_id
    ).order_by(
        Resume.created_at.desc()
    ).first()

    # --------------------------------------
    # Explore Data
    # --------------------------------------

    careers = Career.query.limit(6).all()

    internships = Internship.query.limit(5).all()

    scholarships = Scholarship.query.limit(5).all()

    exams = GovernmentExam.query.limit(5).all()

    # --------------------------------------
    # Learning Progress
    # --------------------------------------

    progress_count = LearningProgress.query.filter_by(
        user_id=user_id
    ).count()

    total_steps = CareerRoadmap.query.count()

    if total_steps == 0:

        progress_percentage = 0

    else:

        progress_percentage = round(
            (progress_count / total_steps) * 100,
            1
        )

    # --------------------------------------
    # Profile Completion
    # --------------------------------------

    profile = StudentProfile.query.filter_by(
        user_id=user_id
    ).first()

    completion = 0

    if profile:

        fields = [

            profile.phone,
            profile.state,
            profile.district,
            profile.current_class,
            profile.school_college,
            profile.career_goal,
            profile.interests,
            profile.strengths,
            profile.weaknesses,
            profile.learning_style

        ]

        filled = len([
            x for x in fields if x
        ])

        completion = int(
            (filled / len(fields)) * 100
        )

    # --------------------------------------
    # AI Recommendations
    # --------------------------------------

    recommendations = []

    if latest:

        try:

            recommendations = AIRecommendationService.recommend(
                latest.recommended_category
            )

        except Exception:

            recommendations = []

    # --------------------------------------
    # Render Dashboard
    # --------------------------------------

    return render_template(

        "student/dashboard.html",

        user=user,

        assessments=assessments,

        history=history,

        latest=latest,

        matches=matches,

        saved=saved,

        resume=resume,

        careers=careers,

        internships=internships,

        scholarships=scholarships,

        exams=exams,

        progress_count=progress_count,

        progress_percentage=progress_percentage,

        completion=completion,

        recommendations=recommendations

    )


# ==========================================
# Save Career
# ==========================================

@student.route("/save-career/<int:career_id>")
def save_career(career_id):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    existing = SavedCareer.query.filter_by(

        user_id=session["user_id"],

        career_id=career_id

    ).first()

    if existing:

        flash(
            "Career already saved.",
            "warning"
        )

    else:

        saved = SavedCareer(

            user_id=session["user_id"],

            career_id=career_id

        )

        db.session.add(saved)

        db.session.commit()

        flash(
            "Career saved successfully.",
            "success"
        )

    return redirect(
        request.referrer
        or url_for("career.career_list")
    )


# ==========================================
# Remove Saved Career
# ==========================================

@student.route("/remove-career/<int:id>")
def remove_saved_career(id):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    saved = SavedCareer.query.get_or_404(id)

    if saved.user_id != session.get("user_id"):

        flash(
            "Unauthorized action.",
            "danger"
        )

        return redirect(
            url_for("student.dashboard")
        )

    db.session.delete(saved)

    db.session.commit()

    flash(
        "Career removed successfully.",
        "success"
    )

    return redirect(
        url_for("student.dashboard")
    )