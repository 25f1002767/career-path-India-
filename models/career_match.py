from extensions import db


class CareerMatch(db.Model):

    __tablename__ = "career_matches"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id"),
        nullable=False
    )

    match_percentage = db.Column(
        db.Float,
        nullable=False
    )

    recommendation_reason = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    career = db.relationship(
        "Career",
        backref="career_matches"
    )