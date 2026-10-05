from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request
)
from sqlalchemy import or_

from models.career import Career
from models.college import College
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship

main = Blueprint(
    "main",
    __name__
)


@main.route("/")
def index():
    counts = {
        "careers": Career.query.count(),
        "colleges": College.query.count(),
        "exams": GovernmentExam.query.count(),
        "opportunities": Scholarship.query.count() + Internship.query.count()
    }
    return render_template("home/hero.html", counts=counts)


@main.route("/dashboard")
def dashboard():
    return redirect(url_for("dashboard.home"))


@main.route("/ai-mentor")
def ai_mentor():
    return redirect(url_for("chatbot.home"))


@main.route("/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("search/results.html", query="", total_results=0)

    pattern = f"%{query}%"

    careers = Career.query.filter(
        or_(
            Career.title.ilike(pattern),
            Career.category.ilike(pattern),
            Career.description.ilike(pattern),
            Career.skills_required.ilike(pattern)
        )
    ).limit(8).all()

    colleges = College.query.filter(
        or_(
            College.name.ilike(pattern),
            College.city.ilike(pattern),
            College.state.ilike(pattern),
            College.course.ilike(pattern)
        )
    ).limit(8).all()

    exams = GovernmentExam.query.filter(
        or_(
            GovernmentExam.exam_name.ilike(pattern),
            GovernmentExam.category.ilike(pattern),
            GovernmentExam.description.ilike(pattern)
        )
    ).limit(8).all()

    scholarships = Scholarship.query.filter(
        or_(
            Scholarship.title.ilike(pattern),
            Scholarship.provider.ilike(pattern),
            Scholarship.category.ilike(pattern)
        )
    ).limit(8).all()

    internships = Internship.query.filter(
        or_(
            Internship.title.ilike(pattern),
            Internship.company.ilike(pattern),
            Internship.skills.ilike(pattern),
            Internship.domain.ilike(pattern)
        )
    ).limit(8).all()

    total_results = len(careers) + len(colleges) + len(exams) + len(scholarships) + len(internships)

    return render_template(
        "search/results.html",
        query=query,
        careers=careers,
        colleges=colleges,
        exams=exams,
        scholarships=scholarships,
        internships=internships,
        total_results=total_results
    )