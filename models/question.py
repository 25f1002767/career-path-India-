from extensions import db
from datetime import datetime


class AssessmentQuestion(db.Model):

    __tablename__ = "assessment_questions"

    id = db.Column(db.Integer, primary_key=True)

    question = db.Column(db.String(300), nullable=False)

    category = db.Column(db.String(50), nullable=False)

    option_a = db.Column(db.String(200), nullable=False)

    option_b = db.Column(db.String(200), nullable=False)

    option_c = db.Column(db.String(200), nullable=False)

    option_d = db.Column(db.String(200), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )