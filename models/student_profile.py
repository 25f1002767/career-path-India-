from extensions import db


class StudentProfile(db.Model):

    __tablename__ = "student_profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    phone = db.Column(
        db.String(15)
    )

    state = db.Column(
        db.String(100)
    )

    district = db.Column(
        db.String(100)
    )

    current_class = db.Column(
        db.String(100)
    )

    school_college = db.Column(
        db.String(200)
    )

    career_goal = db.Column(
        db.String(150)
    )

    interests = db.Column(
        db.Text
    )

    strengths = db.Column(
        db.Text
    )

    weaknesses = db.Column(
        db.Text
    )

    learning_style = db.Column(
        db.String(100)
    )

    profile_completed = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )