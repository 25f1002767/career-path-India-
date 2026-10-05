from extensions import db


class CareerRoadmap(db.Model):
    """
    Structured roadmap for a career pathway.
    Supports multiple routes (Path A: Common, Path B: Alternative, Path C: Specialized)
    and class-wise starting points (Class 10, Class 12, Graduation, Working Professional).
    """
    __tablename__ = "career_roadmaps"

    id = db.Column(db.Integer, primary_key=True)

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Route metadata
    path_name = db.Column(db.String(150), default="Direct Academic Route")
    path_type = db.Column(db.String(50), default="COMMON", index=True)  # COMMON, ALTERNATIVE, SPECIALIZED
    starting_point = db.Column(db.String(100), default="Class 12", index=True)  # Class 10, Class 12, Graduation, Working Professional

    overview = db.Column(db.Text)
    required_skills = db.Column(db.Text)
    best_colleges = db.Column(db.Text)
    recommended_courses = db.Column(db.Text)
    projects = db.Column(db.Text)
    internships = db.Column(db.Text)
    salary = db.Column(db.String(100))
    future_scope = db.Column(db.Text)
    top_companies = db.Column(db.Text)
    roadmap_steps = db.Column(db.Text)  # JSON or newline-separated structured steps

    # Parent Career Relationship
    career = db.relationship(
        "Career",
        backref=db.backref(
            "roadmaps",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return f"<CareerRoadmap Career:{self.career_id} [{self.path_type}] - {self.path_name}>"