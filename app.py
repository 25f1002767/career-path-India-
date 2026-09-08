from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db


# ============================================================
# IMPORT MODELS
# ============================================================

from models.user import User
from models.career import Career
from models.assessment import AssessmentResult
from models.question import AssessmentQuestion
from models.roadmap import CareerRoadmap
from models.college import College
from models.scholarship import Scholarship
from models.internship import Internship
from models.exam import GovernmentExam
from models.saved_career import SavedCareer
from models.resume import Resume
from models.career_skill import CareerSkill
from models.website_visit import WebsiteVisit


# ============================================================
# IMPORT ROUTES
# ============================================================

from routes.main import main
from routes.auth import auth
from routes.student import student
from routes.career import career
from routes.assessment import assessment
from routes.admin import admin
from routes.college import college
from routes.scholarship import scholarship
from routes.internship import internship
from routes.exam import exam
from routes.chatbot import chatbot
from routes.resume import resume
from routes.roadmap import roadmap
from routes.dashboard import dashboard
from routes.report import report
from routes.opportunity import opportunity
from routes.profile import profile


# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

db.init_app(app)


# ============================================================
# GLOBAL LOGIN PROTECTION
# ============================================================

@app.before_request
def require_login():

    """
    Protect the entire website.

    Public:
        - Home
        - Login
        - Register
        - Logout
        - Static files

    Everything else requires login.
    """

    # Endpoints that are allowed without login
    public_endpoints = {
        "landing",
        "main.index",
        "auth.login",
        "auth.register",
        "auth.logout",
        "static"
    }

    # Allow public endpoints
    if request.endpoint in public_endpoints:
        return

    # If user is logged in, allow access
    if session.get("user_id"):
        return

    # User is not logged in
    flash(
        "Please login first to access this section.",
        "warning"
    )

    return redirect(url_for("auth.login"))


# ============================================================
# WEBSITE VISIT TRACKER
# ============================================================

@app.before_request
def track_website_visit():

    """
    Count website visits.

    Static files and admin pages are excluded.
    """

    # Ignore static files
    if request.path.startswith("/static/"):
        return

    # Ignore admin pages
    if request.path.startswith("/admin"):
        return

    try:

        visit = WebsiteVisit()

        db.session.add(visit)
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            "VISIT TRACKING ERROR:",
            e
        )


# ============================================================
# PROTECTED EXTERNAL LINKS
# ============================================================

@app.route("/go/scholarships")
def go_scholarships():

    """
    Open the National Scholarship Portal.

    Login is automatically checked by
    the global require_login() function.
    """

    return redirect(
        "https://scholarships.gov.in/"
    )


@app.route("/go/internships")
def go_internships():

    """
    Open the AICTE Internship Portal.

    Login is automatically checked by
    the global require_login() function.
    """

    return redirect(
        "https://internship.aicte-india.org/"
    )


@app.route("/go/ai-assistant")
def go_ai_assistant():

    """
    Open the MPath Career Counselling AI Assistant.

    Login is automatically checked by
    the global require_login() function.
    """

    return redirect(
        "https://career-path-india-3.onrender.com/"
    )


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

with app.app_context():

    db.create_all()

    # ========================================================
    # CREATE / UPDATE ADMIN
    # ========================================================

    admin_user = User.query.filter_by(
        email="admin@example.com"
    ).first()

    if not admin_user:

        admin_user = User(
            full_name="Admin User",
            email="admin@example.com",
            password_hash=generate_password_hash(
                "admin123"
            ),
            role="admin",
            is_active=True
        )

        db.session.add(admin_user)

    else:

        # Make sure existing admin remains administrator
        admin_user.role = "admin"
        admin_user.is_active = True

    db.session.commit()


# ============================================================
# REGISTER BLUEPRINTS
# ============================================================

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(student)
app.register_blueprint(career)
app.register_blueprint(assessment)
app.register_blueprint(admin)
app.register_blueprint(college)
app.register_blueprint(scholarship)
app.register_blueprint(internship)
app.register_blueprint(exam)
app.register_blueprint(chatbot)
app.register_blueprint(resume)
app.register_blueprint(roadmap)
app.register_blueprint(dashboard)
app.register_blueprint(report)
app.register_blueprint(opportunity)
app.register_blueprint(profile)


# ============================================================
# LANDING / HOME PAGE
# ============================================================

@app.route("/")
def landing():

    """
    Home page is PUBLIC.

    Visitors can explore the homepage without login.
    """

    return render_template(
        "home/hero.html"
    )


# ============================================================
# ERROR PAGES
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "errors/404.html"
    ), 404


@app.errorhandler(500)
def server_error(error):

    return render_template(
        "errors/500.html"
    ), 500


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
