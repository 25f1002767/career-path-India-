from extensions import db


class User(db.Model):

    __tablename__ = "users"

    # ==========================
    # Columns
    # ==========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="student"
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # ==========================
    # Relationships
    # ==========================

    profile = db.relationship(
        "StudentProfile",
        backref="user",
        uselist=False
    )

    assessment_results = db.relationship(
        "AssessmentResult",
        backref="user",
        lazy=True
    )

    saved_careers = db.relationship(
        "SavedCareer",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    resumes = db.relationship(
        "Resume",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )
    career_matches = db.relationship(
    "CareerMatch",
    backref="user",
    lazy=True,
    cascade="all, delete-orphan"
)
learning_progress = db.relationship(
    "LearningProgress",
    backref="student",
    lazy=True,
    cascade="all, delete-orphan"
)



