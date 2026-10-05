from extensions import db


class SavedOpportunity(db.Model):
    __tablename__ = "saved_opportunities"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    opportunity_type = db.Column(
        db.String(50),
        nullable=False
    )  # "exam", "scholarship", "internship"
    item_id = db.Column(
        db.Integer,
        nullable=False
    )
    title = db.Column(
        db.String(255),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
