from extensions import db


class SavedCollege(db.Model):
    __tablename__ = "saved_colleges"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    college_id = db.Column(
        db.Integer,
        db.ForeignKey("colleges.id"),
        nullable=False,
        index=True
    )
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    college = db.relationship("College", backref="saved_by")
