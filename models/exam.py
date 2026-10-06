from datetime import datetime
from extensions import db


class GovernmentExam(db.Model):
    """
    Comprehensive National Career Opportunity & Examination Intelligence Model.
    Supports National and State-level Examinations, Government Recruitments,
    Entrance Tests, Defence Entries, PSU Recruitment, Research Fellowships,
    Apprenticeships, and Higher Education pathways.
    """
    __tablename__ = "government_exams"

    id = db.Column(db.Integer, primary_key=True)

    # Core Identification
    exam_name = db.Column(db.String(250), nullable=False, index=True)
    full_name = db.Column(db.String(300), nullable=True)
    short_name = db.Column(db.String(100), nullable=True, index=True)
    slug = db.Column(db.String(250), nullable=True, unique=True, index=True)
    conducted_by = db.Column(db.String(250), nullable=True, index=True)
    conducting_organisation = db.Column(db.String(300), nullable=True)
    organisation_type = db.Column(db.String(100), default="Government")
    # Government / Statutory Body / Autonomous / PSU / Private / University

    # Types & Categorization
    exam_type = db.Column(db.String(100), default="Recruitment", index=True)
    # Recruitment, Entrance, Eligibility, Competitive, Professional, Apprenticeship, Fellowship
    opportunity_type = db.Column(db.String(100), default="EXAM", index=True)
    # EXAM, ENTRANCE_EXAM, GOVERNMENT_RECRUITMENT, PRIVATE_RECRUITMENT, PSU_RECRUITMENT,
    # DEFENCE_ENTRY, INTERNSHIP, APPRENTICESHIP, SCHOLARSHIP, FELLOWSHIP, CERTIFICATION,
    # COMPETITION, OLYMPIAD, TRAINING, SKILL_PROGRAM, RESEARCH_OPPORTUNITY, HIGHER_EDUCATION, OTHER
    category = db.Column(db.String(100), nullable=True, index=True)
    sub_category = db.Column(db.String(100), nullable=True, index=True)
    description = db.Column(db.Text, nullable=True)

    # Academic Eligibility
    education_level = db.Column(db.String(100), nullable=True, index=True)
    # 10th, 12th, Diploma, Graduate / UG, Post Graduate / PG, Doctorate / PhD
    qualification = db.Column(db.String(250), nullable=True, index=True)
    degree = db.Column(db.String(100), nullable=True)
    diploma = db.Column(db.String(100), nullable=True)
    minimum_qualification = db.Column(db.String(100), nullable=True, index=True)
    preferred_qualification = db.Column(db.String(250), nullable=True)
    streams = db.Column(db.String(250), nullable=True)
    specialisation = db.Column(db.String(250), nullable=True)
    required_skills = db.Column(db.Text, nullable=True)

    # Age & Demographic Criteria
    age_min = db.Column(db.Integer, nullable=True)
    age_max = db.Column(db.Integer, nullable=True)
    age_limit = db.Column(db.String(150), nullable=True)
    age_relaxation = db.Column(db.Text, nullable=True)
    nationality = db.Column(db.String(100), default="Indian")
    gender_eligibility = db.Column(db.String(100), default="All")
    category_eligibility = db.Column(db.String(200), default="General, OBC, SC, ST, EWS")
    pwd_eligibility = db.Column(db.String(100), default="Eligible as per Govt Norms")
    domicile_requirement = db.Column(db.String(200), default="None / All India")
    experience_requirement = db.Column(db.String(200), default="Fresher / None")
    eligibility = db.Column(db.Text, nullable=True)

    # Jurisdiction
    national_or_state = db.Column(db.String(50), default="National", index=True)
    government_or_private = db.Column(db.String(50), default="Government")
    central_or_state = db.Column(db.String(50), default="Central")
    state = db.Column(db.String(100), default="All India", index=True)
    district = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)

    # Process & Pattern
    application_mode = db.Column(db.String(50), default="Online")
    exam_mode = db.Column(db.String(100), default="Computer Based Test (CBT)")
    selection_process = db.Column(db.Text, nullable=True)
    subjects = db.Column(db.Text, nullable=True)
    exam_pattern = db.Column(db.Text, nullable=True)
    number_of_papers = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(100), nullable=True)
    negative_marking = db.Column(db.String(100), nullable=True)
    syllabus = db.Column(db.Text, nullable=True)

    # Interconnections
    career_opportunities = db.Column(db.Text, nullable=True)
    related_courses = db.Column(db.Text, nullable=True)
    related_careers = db.Column(db.Text, nullable=True)

    # Verified Official Portals & Direct Links
    official_website = db.Column(db.String(350), nullable=True)
    official_url = db.Column(db.String(350), nullable=True)
    application_url = db.Column(db.String(350), nullable=True)
    notification_url = db.Column(db.String(350), nullable=True)
    admit_card_url = db.Column(db.String(500), nullable=True)
    result_url = db.Column(db.String(500), nullable=True)
    answer_key_url = db.Column(db.String(500), nullable=True)
    cutoff_url = db.Column(db.String(500), nullable=True)
    previous_papers_url = db.Column(db.String(500), nullable=True)
    syllabus_url = db.Column(db.String(500), nullable=True)
    calendar_url = db.Column(db.String(500), nullable=True)
    url_status = db.Column(db.String(50), default="VALID", index=True)
    # VALID, NEEDS_VERIFICATION, BROKEN, MISSING, REDIRECTED

    # Cycle & Active Dates
    application_start_date = db.Column(db.String(100), nullable=True)
    application_end_date = db.Column(db.String(100), nullable=True)
    exam_date = db.Column(db.String(100), nullable=True)
    frequency = db.Column(db.String(100), default="Annual")
    fee = db.Column(db.String(150), nullable=True)
    vacancies = db.Column(db.String(150), nullable=True)
    salary = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), default="GENERAL_INFORMATION", index=True)
    # Statuses: UPCOMING, APPLICATION_OPEN, APPLICATION_CLOSING_SOON, APPLICATION_CLOSED, EXAM_SCHEDULED, EXAM_COMPLETED, NOTIFICATION_EXPECTED, ARCHIVED, GENERAL_INFORMATION

    # Source & Verification Integrity
    source_id = db.Column(db.Integer, db.ForeignKey("opportunity_sources.id", ondelete="SET NULL"), nullable=True)
    source = db.Column(db.String(255), default="Official Examination Authority")
    source_url = db.Column(db.String(350), nullable=True)
    verification_status = db.Column(db.String(50), default="VERIFIED_OFFICIAL", index=True)
    # VERIFIED_OFFICIAL, VERIFIED_GOVERNMENT, CROSS_CHECKED, NEEDS_REVIEW, UNVERIFIED, STALE, BROKEN, ARCHIVED
    last_verified_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cycles = db.relationship("ExamCycle", backref="exam", lazy="dynamic", cascade="all, delete-orphan", order_by="desc(ExamCycle.cycle_year)")
    trackers = db.relationship("StudentOpportunityTracker", backref="exam", lazy="dynamic", cascade="all, delete-orphan")
    change_logs = db.relationship("OpportunityChangeLog", backref="exam", lazy="dynamic", cascade="all, delete-orphan")

    # Aliases & Compatibility Properties
    @property
    def name(self):
        return self.exam_name

    @name.setter
    def name(self, val):
        self.exam_name = val

    @property
    def conducting_body(self):
        return self.conducting_organisation or self.conducted_by or "Statutory Board"

    @conducting_body.setter
    def conducting_body(self, val):
        self.conducted_by = val
        self.conducting_organisation = val

    @property
    def display_status(self):
        status_map = {
            "APPLICATION_OPEN": ("Applications Open", "success", "check-circle"),
            "APPLICATION_CLOSING_SOON": ("Closing Soon", "warning text-dark", "clock"),
            "UPCOMING": ("Upcoming Cycle", "primary", "calendar"),
            "APPLICATION_CLOSED": ("Application Closed", "danger", "slash"),
            "EXAM_SCHEDULED": ("Exam Scheduled", "info text-dark", "clock"),
            "EXAM_COMPLETED": ("Exam Completed", "secondary", "check"),
            "RESULT_DECLARED": ("Result Declared", "success", "award"),
            "NOTIFICATION_EXPECTED": ("Notification Expected", "secondary", "bell"),
            "GENERAL_INFORMATION": ("General Info", "secondary", "info"),
            "ARCHIVED": ("Archived", "secondary", "archive")
        }
        return status_map.get(self.status, (self.status or "General Info", "secondary", "info"))

    @property
    def latest_cycle(self):
        return self.cycles.first()

    @property
    def verified_badge(self):
        if self.verification_status in ["VERIFIED_OFFICIAL", "VERIFIED"]:
            return ("Verified Official Source", "success", "shield-check")
        elif self.verification_status == "VERIFIED_GOVERNMENT":
            return ("Verified Government Directory", "primary", "shield")
        elif self.verification_status == "CROSS_CHECKED":
            return ("Cross-Checked", "info", "check")
        return ("Needs Review", "warning", "alert-circle")