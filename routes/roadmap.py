from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from extensions import db

from models.career import Career
from models.roadmap import CareerRoadmap
from models.learning_progress import LearningProgress

roadmap = Blueprint(
    "roadmap",
    __name__,
    url_prefix="/roadmap"
)


@roadmap.route("/<int:career_id>")
def details(career_id):

    career = Career.query.get_or_404(career_id)

    roadmap_data = CareerRoadmap.query.filter_by(
        career_id=career.id
    ).first()

    progress = []

    if "user_id" in session:

        progress = LearningProgress.query.filter_by(
            user_id=session["user_id"],
            career_id=career.id
        ).all()

    return render_template(
        "roadmap/details.html",
        career=career,
        roadmap=roadmap_data,
        progress=progress
    )


@roadmap.route("/complete/<int:career_id>/<step>")
def complete_step(career_id, step):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    existing = LearningProgress.query.filter_by(
        user_id=session["user_id"],
        career_id=career_id,
        roadmap_step=step
    ).first()

    if not existing:

        item = LearningProgress(
            user_id=session["user_id"],
            career_id=career_id,
            roadmap_step=step,
            is_completed=True
        )

        db.session.add(item)

        db.session.commit()

    return redirect(
        url_for(
            "roadmap.details",
            career_id=career_id
        )
    )