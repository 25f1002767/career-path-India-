from extensions import db


class Scholarship(db.Model):

    __tablename__ = "scholarships"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    provider = db.Column(db.String(200))

    category = db.Column(db.String(100))

    eligibility = db.Column(db.Text)

    amount = db.Column(db.String(100))

    deadline = db.Column(db.String(100))

    website = db.Column(db.String(255))

    description = db.Column(db.Text)