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

    domain = db.Column(
        db.String(100),
        nullable=True
    )

    skills = db.Column(
        db.String(255),
        nullable=True
    )

    source = db.Column(
        db.String(255),
        default="AICTE & Official Career Portals"
    )

    official_url = db.Column(
        db.String(300),
        nullable=True
    )

    verification_status = db.Column(
        db.String(50),
        default="VERIFIED",
        index=True
    )

    last_verified_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )