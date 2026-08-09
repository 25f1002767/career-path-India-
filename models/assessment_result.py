from extensions import db


class AssessmentResult(db.Model):

    __tablename__ = "assessment_results"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    career_type = db.Column(
        db.String(150)
    )

    score = db.Column(
        db.Integer
    )

    personality = db.Column(
        db.String(100)
    )

    recommendation = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )