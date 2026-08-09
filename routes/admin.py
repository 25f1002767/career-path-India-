from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from extensions import db

from models.user import User
from models.career import Career
from models.college import College
from models.scholarship import Scholarship
from models.internship import Internship
from models.exam import GovernmentExam
from models.assessment import AssessmentResult
from models.roadmap import CareerRoadmap

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.route("/")
def dashboard():

    stats = {

        "users": User.query.count(),

        "careers": Career.query.count(),

        "colleges": College.query.count(),

        "scholarships": Scholarship.query.count(),

        "internships": Internship.query.count(),

        "exams": GovernmentExam.query.count(),

        "assessments": AssessmentResult.query.count()

    }

    recent_users = User.query.order_by(
        User.created_at.desc()
    ).limit(5).all()

    recent_careers = Career.query.order_by(
        Career.created_at.desc()
    ).limit(5).all()

    return render_template(

        "admin/dashboard.html",

        stats=stats,

        recent_users=recent_users,

        recent_careers=recent_careers

    )

@admin.route("/careers")
def careers():

    search = request.args.get("search", "")

    if search:
        careers = Career.query.filter(
            Career.title.contains(search)
        ).all()
    else:
        careers = Career.query.order_by(
            Career.title.asc()
        ).all()

    return render_template(
        "admin/careers.html",
        careers=careers,
        search=search
    )


@admin.route("/careers/add", methods=["GET", "POST"])
def add_career():

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]
        description = request.form["description"]
        average_salary = request.form["average_salary"]
        future_scope = request.form["future_scope"]
        education_required = request.form["education_required"]
        skills_required = request.form["skills_required"]

        slug = title.lower().replace(" ", "-")

        career = Career(
            title=title,
            slug=slug,
            category=category,
            description=description,
            average_salary=average_salary,
            future_scope=future_scope,
            education_required=education_required,
            skills_required=skills_required
        )

        db.session.add(career)
        db.session.commit()

        flash("Career Added Successfully!", "success")

        return redirect(url_for("admin.careers"))

    return render_template("admin/add_career.html")


@admin.route("/careers/edit/<int:id>", methods=["GET", "POST"])
def edit_career(id):

    career = Career.query.get_or_404(id)

    if request.method == "POST":

        career.title = request.form["title"]
        career.category = request.form["category"]
        career.description = request.form["description"]
        career.average_salary = request.form["average_salary"]
        career.future_scope = request.form["future_scope"]
        career.education_required = request.form["education_required"]
        career.skills_required = request.form["skills_required"]

        db.session.commit()

        flash("Career Updated Successfully!", "success")

        return redirect(url_for("admin.careers"))

    return render_template(
        "admin/edit_career.html",
        career=career
    )


@admin.route("/careers/delete/<int:id>")
def delete_career(id):

    career = Career.query.get_or_404(id)

    db.session.delete(career)

    db.session.commit()

    flash("Career Deleted Successfully!", "warning")

    return redirect(url_for("admin.careers"))
# ==========================================
# Roadmap List
# ==========================================

@admin.route("/roadmaps")
def roadmaps():

    roadmaps = CareerRoadmap.query.all()

    return render_template(
        "admin/roadmaps.html",
        roadmaps=roadmaps
    )


# ==========================================
# Add Roadmap
# ==========================================

@admin.route("/roadmaps/add", methods=["GET", "POST"])
def add_roadmap():

    careers = Career.query.order_by(Career.title).all()

    if request.method == "POST":

        roadmap = CareerRoadmap(

            career_id=request.form["career_id"],

            overview=request.form["overview"],

            required_skills=request.form["required_skills"],

            best_colleges=request.form["best_colleges"],

            recommended_courses=request.form["recommended_courses"],

            projects=request.form["projects"],

            internships=request.form["internships"],

            salary=request.form["salary"],

            future_scope=request.form["future_scope"],

            top_companies=request.form["top_companies"],

            roadmap_steps=request.form["roadmap_steps"]

        )

        db.session.add(roadmap)
        db.session.commit()

        return redirect(url_for("admin.roadmaps"))

    return render_template(
        "admin/add_roadmap.html",
        careers=careers
    )
# ==========================================
# College List
# ==========================================

@admin.route("/colleges")
def colleges():

    colleges = College.query.order_by(
        College.name
    ).all()

    return render_template(
        "admin/colleges.html",
        colleges=colleges
    )


# ==========================================
# Add College
# ==========================================

@admin.route("/colleges/add", methods=["GET", "POST"])
def add_college():

    if request.method == "POST":

        college = College(

            name=request.form["name"],

            city=request.form["city"],

            state=request.form["state"],

            college_type=request.form["college_type"],

            course=request.form["course"],

            fees=request.form["fees"],

            placement=request.form["placement"],

            highest_package=request.form["highest_package"],

            average_package=request.form["average_package"],

            website=request.form["website"],

            description=request.form["description"]

        )

        db.session.add(college)

        db.session.commit()

        flash(
            "College Added Successfully",
            "success"
        )

        return redirect(
            url_for("admin.colleges")
        )

    return render_template(
        "admin/add_college.html"
    )


# ==========================================
# Delete College
# ==========================================

@admin.route("/colleges/delete/<int:id>")
def delete_college(id):

    college = College.query.get_or_404(id)

    db.session.delete(college)

    db.session.commit()

    flash(
        "College Deleted",
        "success"
    )

    return redirect(
        url_for("admin.colleges")
    )