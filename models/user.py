from extensions import db


class User(db.Model):

    __tablename__ = "users"

    # =====================================================
    # BASIC ACCOUNT INFORMATION
    # =====================================================

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
        default="student",
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    # =====================================================
    # STUDENT INFORMATION
    # =====================================================

    contact_number = db.Column(
        db.String(20),
        nullable=True
    )

    class_grade = db.Column(
        db.String(50),
        nullable=True
    )

    stream = db.Column(
        db.String(50),
        nullable=True
    )

    college_name = db.Column(
        db.String(200),
        nullable=True
    )

    course = db.Column(
        db.String(150),
        nullable=True
    )

    passing_year = db.Column(
        db.String(10),
        nullable=True
    )

    state = db.Column(
        db.String(100),
        nullable=True
    )

    district = db.Column(
        db.String(100),
        nullable=True
    )

    career_interest = db.Column(
        db.String(200),
        nullable=True
    )


    # =====================================================
    # RELATIONSHIPS
    # =====================================================

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
    back_populates="user",
    lazy=True,
    cascade="all, delete-orphan"

    )