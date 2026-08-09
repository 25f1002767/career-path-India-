from app import app
from models.question import AssessmentQuestion

with app.app_context():
    print("Total Questions:", AssessmentQuestion.query.count())