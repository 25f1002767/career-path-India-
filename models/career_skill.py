from extensions import db


class CareerSkill(db.Model):
    """
    Structured skill profile for Careers.
    Categorized into Technical, Soft, and Tools to support Skill -> Career discovery.
    """
    __tablename__ = "career_skills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    skill_name = db.Column(
        db.String(150),
        nullable=False,
        index=True
    )

    skill_level = db.Column(
        db.String(50),
        default="Beginner"
    )

    # Technical, Soft, Tool, Domain
    skill_category = db.Column(
        db.String(50),
        default="Technical",
        index=True
    )

    # Essential, Recommended, Good to have
    importance = db.Column(
        db.String(50),
        default="Essential"
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

    def __repr__(self):
        return f"<CareerSkill {self.skill_name} ({self.skill_category}) for Career:{self.career_id}>"