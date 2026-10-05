from datetime import datetime
from extensions import db


class GovernmentExam(db.Model):
    """
    Comprehensive, scalable examination discovery model for Indian Examinations.
    Supports National and State-level Recruitment, Entrance, Eligibility, Competitive,
    and Professional examinations.
    """
    __tablename__ = "government_exams"

    id = db.Column(db.Integer, primary_key=True)

    # Core Identification
    exam_name = db.Column(db.String(250), nullable=False, index=True)
    short_name = db.Column(db.String(100), nullable=True, index=True)
    conducted_by = db.Column(db.String(250), nullable=True, index=True)

    # Types & Hierarchy
    exam_type = db.Column(db.String(100), default="Recruitment", index=True)
    # Types: Entrance, Recruitment, Eligibility, Competitive, Professional, University Entrance, Scholarship
    category = db.Column(db.String(100), nullable=True, index=True)
    sub_category = db.Column(db.String(100), nullable=True, index=True)
    description = db.Column(db.Text, nullable=True)

    # Academic & Age Criteria
    qualification = db.Column(db.String(250), nullable=True, index=True)
    minimum_qualification = db.Column(db.String(100), nullable=True, index=True)
    streams = db.Column(db.String(250), nullable=True)
    age_min = db.Column(db.Integer, nullable=True)
    age_max = db.Column(db.Integer, nullable=True)
    age_limit = db.Column(db.String(150), nullable=True)
    eligibility = db.Column(db.Text, nullable=True)

    # Jurisdiction
    national_or_state = db.Column(db.String(50), default="National", index=True)
    state = db.Column(db.String(100), default="All India", index=True)
    region = db.Column(db.String(100), nullable=True)

    # Process & Pattern
    application_mode = db.Column(db.String(50), default="Online")
    exam_mode = db.Column(db.String(100), default="Computer Based Test (CBT)")
    selection_process = db.Column(db.Text, nullable=True)
    subjects = db.Column(db.Text, nullable=True)
    exam_pattern = db.Column(db.Text, nullable=True)
    syllabus = db.Column(db.Text, nullable=True)

    # Career & Education Interconnections
    career_opportunities = db.Column(db.Text, nullable=True)
    related_courses = db.Column(db.Text, nullable=True)
    related_careers = db.Column(db.Text, nullable=True)

    # Verified Official Portals
    official_website = db.Column(db.String(350), nullable=True)
    official_url = db.Column(db.String(350), nullable=True)
    application_url = db.Column(db.String(350), nullable=True)
    notification_url = db.Column(db.String(350), nullable=True)

    # Examination Cycle & Important Metadata (Verified only)
    application_start_date = db.Column(db.String(100), nullable=True)
    application_end_date = db.Column(db.String(100), nullable=True)
    exam_date = db.Column(db.String(100), nullable=True)
    frequency = db.Column(db.String(100), default="Annual")
    fee = db.Column(db.String(150), nullable=True)
    vacancies = db.Column(db.String(150), nullable=True)
    salary = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), default="GENERAL_INFORMATION", index=True)
    # Statuses: UPCOMING, APPLICATION_OPEN, APPLICATION_CLOSED, EXAM_COMPLETED, NOTIFICATION_EXPECTED, ARCHIVED, GENERAL_INFORMATION

    # Source & Verification Integrity
    source = db.Column(db.String(255), default="Official Examination Authority")
    source_url = db.Column(db.String(350), nullable=True)
    verification_status = db.Column(db.String(50), default="VERIFIED", index=True)
    last_verified_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Aliases & Convenience Helpers
    @property
    def name(self):
        return self.exam_name

    @name.setter
    def name(self, val):
        self.exam_name = val

    @property
    def conducting_body(self):
        return self.conducted_by or "Statutory Board"

    @conducting_body.setter
    def conducting_body(self, val):
        self.conducted_by = val

    @property
    def display_status(self):
        status_map = {
            "APPLICATION_OPEN": ("Applications Open", "success", ""),
            "UPCOMING": ("Upcoming Cycle", "warning text-dark", ""),
            "APPLICATION_CLOSED": ("Application Closed", "danger", ""),
            "EXAM_COMPLETED": ("Exam Completed", "secondary", ""),
            "NOTIFICATION_EXPECTED": ("Notification Expected", "info text-dark", ""),
            "GENERAL_INFORMATION": ("General Info", "light text-dark border", ""),
            "ARCHIVED": ("Archived", "secondary", "")
        }
        return status_map.get(self.status, (self.status or "General Info", "light text-dark border", ""))