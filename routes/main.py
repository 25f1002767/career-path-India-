from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)

main = Blueprint(
    "main",
    __name__
)


@main.route("/")
def index():

    return render_template("index.html")


@main.route("/dashboard")
def dashboard():

    return redirect(
        url_for("dashboard.home")
    )