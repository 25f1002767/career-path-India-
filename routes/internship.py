from flask import Blueprint, render_template

from services.knowledge.internship_service import internship_service

internship = Blueprint(
    "internship",
    __name__,
    url_prefix="/internships"
)


@internship.route("/")
def internship_list():

    skills = ["Python", "Machine Learning"]

    internships = internship_service.recommend(skills)

    return render_template(
        "internship/list.html",
        internships=internships,
        search=""
    )