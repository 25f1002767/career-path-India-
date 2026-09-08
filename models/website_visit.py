from extensions import db


class WebsiteVisit(db.Model):
    __tablename__ = "website_visits"

    id = db.Column(db.Integer, primary_key=True)

    visited_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )