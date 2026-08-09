from flask import (
    Blueprint,
    session,
    send_file,
    redirect,
    url_for
)

from models.user import User
from models.assessment import AssessmentResult

from services.ai.context_builder import build_student_context
from services.recommendation_engine import recommend_best_careers
from services.pdf_report import generate_report

report = Blueprint(
    "report",
    __name__,
    url_prefix="/report"
)


@report.route("/career")

def career_report():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    user = User.query.get(
        session["user_id"]
    )

    assessment = AssessmentResult.query.filter_by(

        user_id=user.id

    ).order_by(

        AssessmentResult.id.desc()

    ).first()

    context = build_student_context(user.id)

    recommendations = recommend_best_careers(context)

    filename = "career_report.pdf"

    generate_report(

        user,

        assessment,

        recommendations,

        filename

    )

    return send_file(

        filename,

        as_attachment=True

    )