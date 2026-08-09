from extensions import db


class CareerSkill(db.Model):

    __tablename__ = "career_skills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id"),
        nullable=False
    )

    skill_name = db.Column(
        db.String(150),
        nullable=False
    )

    skill_level = db.Column(
        db.String(50),
        default="Beginner"
    )

    is_required = db.Column(
        db.Boolean,
        default=True
    )

    career = db.relationship(
        "Career",
        backref=db.backref(
            "skills",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )