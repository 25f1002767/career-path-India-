from extensions import db


class Internship(db.Model):

    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    company = db.Column(db.String(150))

    location = db.Column(db.String(150))

    mode = db.Column(db.String(50))

    stipend = db.Column(db.String(100))

    duration = db.Column(db.String(100))

    eligibility = db.Column(db.Text)

    apply_link = db.Column(db.String(300))

    description = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )