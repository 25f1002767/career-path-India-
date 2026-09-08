from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db
from models.user import User


auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# ======================================
# Login
# ======================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    try:

        if request.method == "POST":

            email = request.form.get(
                "email",
                ""
            ).strip().lower()

            password = request.form.get(
                "password",
                ""
            )

            # Find user by email
            user = User.query.filter_by(
                email=email
            ).first()

            # ----------------------------------
            # User does not exist
            # ----------------------------------

            if not user:

                flash(
                    "Invalid email or password.",
                    "danger"
                )

            # ----------------------------------
            # Wrong password
            # ----------------------------------

            elif not check_password_hash(
                user.password_hash,
                password
            ):

                flash(
                    "Invalid email or password.",
                    "danger"
                )

            # ----------------------------------
            # Account is inactive
            # ----------------------------------

            elif not user.is_active:

                flash(
                    "Your account has been deactivated. Please contact the administrator.",
                    "warning"
                )

            # ----------------------------------
            # Login successful
            # ----------------------------------

            else:

                session["user_id"] = user.id
                session["user_name"] = user.full_name
                session["role"] = user.role

                flash(
                    "Login Successful!",
                    "success"
                )

                # Admin → Admin Dashboard
                if user.role == "admin":

                    return redirect(
                        url_for("admin.dashboard")
                    )

                # Student → Student Dashboard
                return redirect(
                    url_for("dashboard.home")
                )

        return render_template(
            "auth/login.html"
        )

    except Exception as e:

        print("LOGIN ERROR:", e)

        return f"Login Error: {e}", 500


# ======================================
# Register
# ======================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    try:

        if request.method == "POST":

            # ----------------------------------
            # Get form data
            # ----------------------------------

            full_name = request.form.get(
                "full_name",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip().lower()

            contact_number = request.form.get(
                "contact_number",
                ""
            ).strip()

            class_grade = request.form.get(
                "class_grade",
                ""
            ).strip()

            stream = request.form.get(
                "stream",
                ""
            ).strip()

            college_name = request.form.get(
                "college_name",
                ""
            ).strip()

            course = request.form.get(
                "course",
                ""
            ).strip()

            passing_year = request.form.get(
                "passing_year",
                ""
            ).strip()

            state = request.form.get(
                "state",
                ""
            ).strip()

            district = request.form.get(
                "district",
                ""
            ).strip()

            career_interest = request.form.get(
                "career_interest",
                ""
            ).strip()

            password = request.form.get(
                "password",
                ""
            )

            confirm_password = request.form.get(
                "confirm_password",
                ""
            )


            # ----------------------------------
            # Required field validation
            # ----------------------------------

            if not full_name:
                flash(
                    "Please enter your full name.",
                    "danger"
                )
                return redirect(
                    url_for("auth.register")
                )

            if not email:
                flash(
                    "Please enter your email address.",
                    "danger"
                )
                return redirect(
                    url_for("auth.register")
                )

            if not password:
                flash(
                    "Please enter a password.",
                    "danger"
                )
                return redirect(
                    url_for("auth.register")
                )


            # ----------------------------------
            # Password length
            # ----------------------------------

            if len(password) < 6:

                flash(
                    "Password must be at least 6 characters long.",
                    "danger"
                )

                return redirect(
                    url_for("auth.register")
                )


            # ----------------------------------
            # Confirm password
            # ----------------------------------

            if password != confirm_password:

                flash(
                    "Passwords do not match.",
                    "danger"
                )

                return redirect(
                    url_for("auth.register")
                )


            # ----------------------------------
            # Check existing email
            # ----------------------------------

            existing_user = User.query.filter_by(
                email=email
            ).first()

            if existing_user:

                flash(
                    "An account with this email already exists.",
                    "danger"
                )

                return redirect(
                    url_for("auth.register")
                )


            # ----------------------------------
            # Hash password
            # ----------------------------------

            hashed_password = generate_password_hash(
                password
            )


            # ----------------------------------
            # Create student account
            # ----------------------------------

            new_user = User(

                full_name=full_name,

                email=email,

                password_hash=hashed_password,

                role="student",

                is_active=True,

                contact_number=contact_number,

                class_grade=class_grade,

                stream=stream,

                college_name=college_name,

                course=course,

                passing_year=passing_year,

                state=state,

                district=district,

                career_interest=career_interest

            )


            db.session.add(new_user)

            db.session.commit()


            # ----------------------------------
            # Registration successful
            # ----------------------------------

            flash(
                "Registration successful! Please login.",
                "success"
            )

            return redirect(
                url_for("auth.login")
            )


        return render_template(
            "auth/register.html"
        )


    except Exception as e:

        # Rollback if database operation fails
        db.session.rollback()

        print(
            "REGISTER ERROR:",
            e
        )

        return f"Register Error: {e}", 500


# ======================================
# Logout
# ======================================

@auth.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out successfully.",
        "info"
    )

    return redirect(
        url_for("main.index")
    )