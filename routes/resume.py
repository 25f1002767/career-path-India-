from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)

from extensions import db
from models.resume import Resume
from services.resume_analyzer import analyze_resume

resume = Blueprint(
    "resume",
    __name__,
    url_prefix="/resume"
)


@resume.route("/", methods=["GET", "POST"])
def upload_resume():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    result = None

    if request.method == "POST":

        resume_text = request.form.get(
            "resume_text"
        )

        if not resume_text:

            flash(
                "Please enter your resume.",
                "danger"
            )

            return redirect(
                url_for("resume.upload_resume")
            )

        # ----------------------------------
        # Analyze Resume
        # ----------------------------------

        result = analyze_resume(
            resume_text
        )

        # ----------------------------------
        # Save Resume Analysis
        # ----------------------------------

        resume_data = Resume(

            user_id=session["user_id"],

            file_name="Manual Resume",

            extracted_text=resume_text,

            score=result["score"],

            missing_skills=", ".join(
                result["missing_skills"]
            ),

            recommended_career=result["career"]

        )

        db.session.add(
            resume_data
        )

        db.session.commit()

        flash(
            "Resume analyzed successfully!",
            "success"
        )

    return render_template(

        "resume/index.html",

        result=result

    )