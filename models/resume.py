from extensions import db


class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    file_name = db.Column(
        db.String(255)
    )

    extracted_text = db.Column(
        db.Text
    )

    score = db.Column(
        db.Integer
    )

    missing_skills = db.Column(
        db.Text
    )

    recommended_career = db.Column(
        db.String(150)
    )

    strengths = db.Column(
        db.Text
    )

    weaknesses = db.Column(
        db.Text
    )

    ats_score = db.Column(
        db.Integer
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )