from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from extensions import db

from models.student_profile import StudentProfile

profile = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


@profile.route("/")
def view_profile():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    profile = StudentProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not profile:

        return redirect(
            url_for("profile.create_profile")
        )

    completion = 0

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

    completed = sum(
        1 for field in fields if field
    )

    completion = int(
        (completed / len(fields)) * 100
    )

    return render_template(

        "profile/view.html",

        profile=profile,

        completion=completion

    )


@profile.route("/create", methods=["GET", "POST"])
def create_profile():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    existing = StudentProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if existing:

        return redirect(
            url_for("profile.view_profile")
        )

    if request.method == "POST":

        profile = StudentProfile(

            user_id=session["user_id"],

            phone=request.form.get("phone"),

            state=request.form.get("state"),

            district=request.form.get("district"),

            current_class=request.form.get("current_class"),

            school_college=request.form.get("school_college"),

            career_goal=request.form.get("career_goal"),

            interests=request.form.get("interests"),

            strengths=request.form.get("strengths"),

            weaknesses=request.form.get("weaknesses"),

            learning_style=request.form.get("learning_style"),

            profile_completed=True

        )

        db.session.add(profile)

        db.session.commit()

        flash(
            "Profile Created Successfully",
            "success"
        )

        return redirect(
            url_for("profile.view_profile")
        )

    return render_template(
        "profile/create.html"
    )


@profile.route("/edit", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    profile = StudentProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not profile:

        return redirect(
            url_for("profile.create_profile")
        )

    if request.method == "POST":

        profile.phone = request.form.get(
            "phone"
        )

        profile.state = request.form.get(
            "state"
        )

        profile.district = request.form.get(
            "district"
        )

        profile.current_class = request.form.get(
            "current_class"
        )

        profile.school_college = request.form.get(
            "school_college"
        )

        profile.career_goal = request.form.get(
            "career_goal"
        )

        profile.interests = request.form.get(
            "interests"
        )

        profile.strengths = request.form.get(
            "strengths"
        )

        profile.weaknesses = request.form.get(
            "weaknesses"
        )

        profile.learning_style = request.form.get(
            "learning_style"
        )

        db.session.commit()

        flash(
            "Profile Updated Successfully",
            "success"
        )

        return redirect(
            url_for("profile.view_profile")
        )

    return render_template(

        "profile/edit.html",

        profile=profile

    )