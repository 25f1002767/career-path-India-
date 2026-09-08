from extensions import db


class LearningProgress(db.Model):

    __tablename__ = "learning_progress"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id"),
        nullable=False
    )

    roadmap_step = db.Column(
        db.String(255),
        nullable=False
    )

    is_completed = db.Column(
        db.Boolean,
        default=False
    )

    completed_at = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Relationship to User
    user = db.relationship(
        "User",
        back_populates="learning_progress"
    )

    # Relationship to Career
    career = db.relationship(
        "Career",
        back_populates="learning_progress"
    )