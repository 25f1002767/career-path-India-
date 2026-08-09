from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from models.user import User
from models.assessment import AssessmentResult
from models.resume import Resume
from models.saved_career import SavedCareer

from services.opportunity_hub import OpportunityHub
from services.eligibility_engine import get_student_profile

dashboard = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard.route("/")
def home():

    # ----------------------------------
    # If user is not logged in
    # Show animated landing page
    # ----------------------------------

    if "user_id" not in session:

        return render_template("home/hero.html")

    # ----------------------------------
    # Current User
    # ----------------------------------

    user = User.query.get(session["user_id"])

    # ----------------------------------
    # Student Profile
    # ----------------------------------

    profile = get_student_profile(user.id)

    # ----------------------------------
    # AI Recommendations
    # ----------------------------------

    if profile:

        recommendations = OpportunityHub.get_all(profile)[:10]

    else:

        recommendations = []

    # ----------------------------------
    # Latest Assessment
    # ----------------------------------

    assessment = AssessmentResult.query.filter_by(
        user_id=user.id
    ).order_by(
        AssessmentResult.id.desc()
    ).first()

    # ----------------------------------
    # Latest Resume
    # ----------------------------------

    resume = Resume.query.filter_by(
        user_id=user.id
    ).order_by(
        Resume.created_at.desc()
    ).first()

    # ----------------------------------
    # Saved Careers Count
    # ----------------------------------

    saved = SavedCareer.query.filter_by(
        user_id=user.id
    ).count()

    # ----------------------------------
    # Render Dashboard
    # ----------------------------------

    return render_template(

        "dashboard/index.html",

        user=user,

        assessment=assessment,

        resume=resume,

        saved=saved,

        recommendations=recommendations

    )