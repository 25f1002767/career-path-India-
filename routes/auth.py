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

            user = User.query.filter_by(
                email=email
            ).first()

            if user and check_password_hash(
                user.password_hash,
                password
            ):

                session["user_id"] = user.id
                session["user_name"] = user.full_name
                session["role"] = user.role

                flash(
                    "Login Successful!",
                    "success"
                )

                # ✅ Correct redirect
                return redirect(
                    url_for("dashboard.home")
                )

            flash(
                "Invalid email or password.",
                "danger"
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

            full_name = request.form.get(
                "full_name",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip().lower()

            password = request.form.get(
                "password",
                ""
            )

            # Check existing user
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

            hashed_password = generate_password_hash(
                password
            )

            new_user = User(
                full_name=full_name,
                email=email,
                password_hash=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

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

        print("REGISTER ERROR:", e)

        return f"Register Error: {e}", 500