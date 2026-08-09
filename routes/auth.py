from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User
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
auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):

            session["user_id"] = user.id
            session["user_name"] = user.full_name
            session["role"] = user.role

            flash("Login Successful!", "success")

            return redirect(url_for("student.dashboard"))
        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name").strip()
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:

            flash("An account with this email already exists.", "danger")

            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")