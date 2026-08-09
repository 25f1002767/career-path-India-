from flask import Flask, render_template

from config import Config
from extensions import db

# ==========================
# Import Models
# ==========================

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

# ==========================
# Import Routes
# ==========================

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

# ==========================
# Create Flask App
# ==========================

app = Flask(__name__)

app.config.from_object(Config)

# ==========================
# Initialize Database
# ==========================

db.init_app(app)


# ==========================
# Register Blueprints
# ==========================

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

# ==========================
# Landing Page
# ==========================

@app.route("/")
def landing():
    return render_template("home/hero.html")

# ==========================
# Error Pages
# ==========================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500

# ==========================
# Run App
# ==========================

if __name__ == "__main__":
    app.run(debug=True)