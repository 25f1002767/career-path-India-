from extensions import db


class CareerRoadmap(db.Model):

    __tablename__ = "career_roadmaps"

    id = db.Column(db.Integer, primary_key=True)

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id"),
        nullable=False
    )

    overview = db.Column(db.Text)

    required_skills = db.Column(db.Text)

    best_colleges = db.Column(db.Text)

    recommended_courses = db.Column(db.Text)

    projects = db.Column(db.Text)

    internships = db.Column(db.Text)

    salary = db.Column(db.String(100))

    future_scope = db.Column(db.Text)

    top_companies = db.Column(db.Text)

    roadmap_steps = db.Column(db.Text)