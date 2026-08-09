from extensions import db


class Career(db.Model):

    __tablename__ = "careers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================
    # Basic Information
    # ==========================================

    title = db.Column(
        db.String(150),
        nullable=False
    )

    slug = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    icon = db.Column(
        db.String(100),
        default="briefcase"
    )

    # ==========================================
    # Career Information
    # ==========================================

    average_salary = db.Column(
        db.String(100)
    )

    future_scope = db.Column(
        db.String(100)
    )

    education_required = db.Column(
        db.String(255)
    )

    skills_required = db.Column(
        db.Text
    )

    experience_level = db.Column(
        db.String(50)
    )

    work_environment = db.Column(
        db.String(100)
    )

    career_growth = db.Column(
        db.String(255)
    )

    # ==========================================
    # India Knowledge Base
    # ==========================================

    entrance_exams = db.Column(
        db.Text
    )

    top_colleges = db.Column(
        db.Text
    )

    top_companies = db.Column(
        db.Text
    )

    government_opportunities = db.Column(
        db.Text
    )

    private_opportunities = db.Column(
        db.Text
    )

    certifications = db.Column(
        db.Text
    )

    roadmap_summary = db.Column(
        db.Text
    )

    projects_to_build = db.Column(
        db.Text
    )

    ai_prompt = db.Column(
        db.Text
    )

    # ==========================================
    # Metadata
    # ==========================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )