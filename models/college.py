from extensions import db


class College(db.Model):

    __tablename__ = "colleges"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    city = db.Column(db.String(100))

    state = db.Column(db.String(100))

    college_type = db.Column(db.String(100))

    course = db.Column(db.String(200))

    fees = db.Column(db.String(100))

    placement = db.Column(db.String(100))

    highest_package = db.Column(db.String(100))

    average_package = db.Column(db.String(100))

    website = db.Column(db.String(255))

    description = db.Column(db.Text)