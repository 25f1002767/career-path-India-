from datetime import datetime
from extensions import db


class ExamCycle(db.Model):
    """
    Represents a specific annual/cyclical recruitment or examination drive (e.g., UPSC CSE 2026, JEE Main 2026 Session 1).
    Preserves historical examination cycles and time-sensitive dates without overwriting the master exam dossier.
    """
    __tablename__ = "exam_cycles"

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("government_exams.id", ondelete="CASCADE"), nullable=False, index=True)
    cycle_year = db.Column(db.Integer, nullable=False, index=True)
    cycle_name = db.Column(db.String(200), nullable=False, index=True)

    # Official Notification Info
    notification_number = db.Column(db.String(150), nullable=True)
    notification_date = db.Column(db.String(100), nullable=True)

    # Important Dates
    application_start_date = db.Column(db.String(100), nullable=True)
    application_end_date = db.Column(db.String(100), nullable=True)
    correction_date = db.Column(db.String(100), nullable=True)
    admit_card_date = db.Column(db.String(100), nullable=True)
    exam_date = db.Column(db.String(100), nullable=True)
    result_date = db.Column(db.String(100), nullable=True)
    counselling_date = db.Column(db.String(100), nullable=True)
    interview_date = db.Column(db.String(100), nullable=True)

    # Cycle specific logistics
    vacancies = db.Column(db.String(150), nullable=True)
    application_fee = db.Column(db.String(200), nullable=True)
    salary_or_stipend = db.Column(db.String(150), nullable=True)

    # Status
    status = db.Column(db.String(50), default="UPCOMING", index=True)
    # UPCOMING, APPLICATION_OPEN, APPLICATION_CLOSING_SOON, APPLICATION_CLOSED, EXAM_SCHEDULED, EXAM_COMPLETED, RESULT_DECLARED, COUNSELLING_OPEN, ARCHIVED

    # Verified Direct Links
    official_notification_url = db.Column(db.String(500), nullable=True)
    official_application_url = db.Column(db.String(500), nullable=True)
    admit_card_url = db.Column(db.String(500), nullable=True)
    result_url = db.Column(db.String(500), nullable=True)
    answer_key_url = db.Column(db.String(500), nullable=True)
    cutoff_url = db.Column(db.String(500), nullable=True)
    syllabus_url = db.Column(db.String(500), nullable=True)
    previous_papers_url = db.Column(db.String(500), nullable=True)

    # Provenance
    source_id = db.Column(db.Integer, db.ForeignKey("opportunity_sources.id", ondelete="SET NULL"), nullable=True)
    verification_status = db.Column(db.String(50), default="VERIFIED_OFFICIAL", index=True)
    last_verified_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to user trackers
    trackers = db.relationship("StudentOpportunityTracker", backref="cycle", lazy="dynamic", cascade="all, delete-orphan")

    @property
    def display_status(self):
        status_map = {
            "APPLICATION_OPEN": ("Applications Open", "success"),
            "APPLICATION_CLOSING_SOON": ("Closing Soon", "warning text-dark"),
            "UPCOMING": ("Upcoming Cycle", "primary"),
            "APPLICATION_CLOSED": ("Application Closed", "danger"),
            "EXAM_SCHEDULED": ("Exam Scheduled", "info text-dark"),
            "EXAM_COMPLETED": ("Exam Completed", "secondary"),
            "RESULT_DECLARED": ("Result Declared", "success"),
            "COUNSELLING_OPEN": ("Counselling Open", "primary"),
            "NOTIFICATION_EXPECTED": ("Notification Expected", "secondary"),
            "ARCHIVED": ("Archived", "secondary")
        }
        return status_map.get(self.status, (self.status or "General Info", "secondary"))
