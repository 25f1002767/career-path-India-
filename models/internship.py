from datetime import datetime, date
import re
from extensions import db


def generate_internship_slug(title: str, company: str, item_id: int = None) -> str:
    combined = f"{title} {company or ''}".strip()
    slug = re.sub(r"[^\w\s-]", "", combined.lower())
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    if item_id:
        slug = f"{slug}-{item_id}"
    return slug[:200]


class Internship(db.Model):
    """
    National Internship Opportunity entity.
    Supports statutory government schemes, PSU programmes, research institutions,
    corporate drives, and university student trainee opportunities across India.
    """
    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)

    # Core Identifiers
    title = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.String(255), nullable=True, unique=True, index=True)
    short_title = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.String(500), nullable=True)

    # Organisation & Scheme Provenance
    organisation_id = db.Column(db.Integer, db.ForeignKey("organisations.id", ondelete="SET NULL"), nullable=True, index=True)
    organisation_name = db.Column(db.String(255), nullable=True, index=True)
    organisation_type = db.Column(db.String(100), default="Corporate", index=True)
    # Government, Ministry, Department, PSU, Corporate, MNC, Indian Company, Startup, MSME, NGO, University, Research Institute
    industry = db.Column(db.String(150), nullable=True, index=True)
    sector = db.Column(db.String(150), nullable=True)
    department = db.Column(db.String(200), nullable=True)
    programme_name = db.Column(db.String(255), nullable=True)
    scheme_name = db.Column(db.String(255), nullable=True, index=True)
    # e.g., TULIP, Indian Army Cyber Cell, C-DAC Tech, NHAI Highways, AMRUT 2.0, NATS

    # Classification & Mode
    internship_type = db.Column(db.String(100), default="Corporate", index=True)
    # Government, PSU, Corporate, Research, NGO, University, Startup
    category = db.Column(db.String(150), default="Technology", index=True)
    sub_category = db.Column(db.String(150), nullable=True, index=True)

    work_mode = db.Column(db.String(50), default="Hybrid", index=True)
    # Remote, Hybrid, Onsite
    location = db.Column(db.String(200), default="India")
    city = db.Column(db.String(100), nullable=True, index=True)
    district = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True, index=True)
    country = db.Column(db.String(100), default="India")
    is_pan_india = db.Column(db.Boolean, default=False)

    # Dates & Timelines
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    application_start_date = db.Column(db.Date, nullable=True)
    application_deadline = db.Column(db.Date, nullable=True, index=True)

    duration_value = db.Column(db.Integer, default=3)
    duration_unit = db.Column(db.String(20), default="Months")
    duration_text = db.Column(db.String(100), default="3 Months")

    # Stipend & Compensation
    stipend = db.Column(db.String(100), default="Provided")
    stipend_min = db.Column(db.Integer, default=0, index=True)
    stipend_max = db.Column(db.Integer, default=0)
    stipend_currency = db.Column(db.String(10), default="INR")
    stipend_type = db.Column(db.String(50), default="Fixed")
    # Fixed, Performance, Unpaid, Expenses Paid
    is_paid = db.Column(db.Boolean, default=True, index=True)
    is_unpaid = db.Column(db.Boolean, default=False)

    # Career & Academic Benefits
    academic_credit_available = db.Column(db.Boolean, default=True)
    ppo_available = db.Column(db.Boolean, default=False, index=True)
    certificate_available = db.Column(db.Boolean, default=True)
    recommendation_letter = db.Column(db.Boolean, default=True)
    working_hours = db.Column(db.String(100), nullable=True)
    weekly_hours = db.Column(db.Integer, default=40)

    # Eligibility & Candidate Profile
    eligibility = db.Column(db.Text, nullable=True)
    minimum_qualification = db.Column(db.String(150), default="Pursuing Undergraduate Degree")
    preferred_qualification = db.Column(db.String(150), nullable=True)
    eligible_streams = db.Column(db.String(255), default="Any")
    eligible_degrees = db.Column(db.String(255), default="B.Tech, BCA, B.Sc, B.Com, BBA, BA")
    eligible_years = db.Column(db.String(100), default="1st, 2nd, 3rd, Final Year")
    minimum_percentage = db.Column(db.Float, default=0.0)
    maximum_age = db.Column(db.Integer, nullable=True)

    # Competencies & Scope
    skills = db.Column(db.String(500), nullable=True)
    technical_skills = db.Column(db.String(500), nullable=True)
    soft_skills = db.Column(db.String(300), nullable=True)
    tools = db.Column(db.String(300), nullable=True)

    responsibilities = db.Column(db.Text, nullable=True)
    learning_outcomes = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    selection_process = db.Column(db.String(255), default="Application Review & Interview")
    number_of_openings = db.Column(db.Integer, default=1)

    # Application & Portal Links
    application_method = db.Column(db.String(50), default="OFFICIAL_PORTAL")
    # OFFICIAL_PORTAL, DIRECT_EMAIL, GOVT_SCHEME_PORTAL
    application_url = db.Column(db.String(500), nullable=True)
    official_application_url = db.Column(db.String(500), nullable=True)
    official_website = db.Column(db.String(500), nullable=True)
    notification_url = db.Column(db.String(500), nullable=True)

    # Provenance & Source Registry
    source_id = db.Column(db.Integer, db.ForeignKey("internship_sources.id", ondelete="SET NULL"), nullable=True, index=True)
    source_name = db.Column(db.String(150), default="Official Portal", index=True)
    source_url = db.Column(db.String(500), nullable=True)
    source_record_id = db.Column(db.String(150), nullable=True, index=True)
    source_type = db.Column(db.String(100), default="STATUTORY_PORTAL")
    source_last_checked = db.Column(db.DateTime, default=datetime.utcnow)

    # Verification & Integrity
    verification_status = db.Column(db.String(50), default="VERIFIED", index=True)
    # VERIFIED, SOURCE_VERIFIED, NEEDS_REVIEW, UNVERIFIED, STALE, EXPIRED, BROKEN, ARCHIVED
    verification_level = db.Column(db.String(50), default="OFFICIAL_AUTHORITY")
    last_verified_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Status
    status = db.Column(db.String(50), default="OPEN", index=True)
    # OPEN, CLOSING_SOON, CLOSED, UPCOMING, EXPIRED, ARCHIVED
    featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # =========================================================================
    # BACKWARD-COMPATIBILITY PROPERTIES
    # =========================================================================
    @property
    def company(self):
        return self.organisation_name or (self.organisation.name if self.organisation else "Organization")

    @company.setter
    def company(self, val):
        self.organisation_name = val

    @property
    def mode(self):
        return self.work_mode or "Hybrid"

    @mode.setter
    def mode(self, val):
        self.work_mode = val

    @property
    def domain(self):
        return self.category or "Technology"

    @domain.setter
    def domain(self, val):
        self.category = val

    @property
    def apply_link(self):
        return self.application_url or self.official_application_url or self.official_website

    @apply_link.setter
    def apply_link(self, val):
        self.application_url = val

    @property
    def official_url(self):
        return self.official_website or self.application_url

    @official_url.setter
    def official_url(self, val):
        self.official_website = val

    @property
    def duration(self):
        return self.duration_text or (f"{self.duration_value} {self.duration_unit or 'Months'}" if self.duration_value else "3 Months")

    @duration.setter
    def duration(self, val):
        self.duration_text = val

    # =========================================================================
    # COMPUTED STATUS & DEADLINE METHODS
    # =========================================================================
    @property
    def display_status(self):
        """
        Dynamically calculates status from application_deadline:
        - If deadline passed -> CLOSED / EXPIRED
        - If deadline within 7 days -> CLOSING_SOON
        - If deadline > 7 days -> OPEN
        """
        today = date.today()
        if self.application_deadline:
            if self.application_deadline < today:
                return ("Application Closed", "danger", "clock")
            days_left = (self.application_deadline - today).days
            if days_left <= 7:
                return (f"Closing in {days_left}d", "warning text-dark", "alert-circle")
            return ("Open for Applications", "success", "check-circle")

        st = (self.status or "OPEN").upper()
        if st == "OPEN":
            return ("Open for Applications", "success", "check-circle")
        elif st == "CLOSING_SOON":
            return ("Closing Soon", "warning text-dark", "alert-circle")
        elif st == "CLOSED":
            return ("Application Closed", "danger", "x-circle")
        elif st == "UPCOMING":
            return ("Upcoming Drive", "info text-dark", "calendar")
        return (st.title(), "secondary", "info")

    @property
    def deadline_text(self):
        if not self.application_deadline:
            return "Refer official portal"
        today = date.today()
        diff = (self.application_deadline - today).days
        if diff < 0:
            return f"Closed on {self.application_deadline.strftime('%d %b %Y')}"
        elif diff == 0:
            return "Closes Today"
        elif diff == 1:
            return "Closes Tomorrow"
        elif diff <= 7:
            return f"Closes in {diff} days"
        return self.application_deadline.strftime("%d %b %Y")

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in re.split(r"[,/|;]", self.skills) if s.strip()]

    @property
    def primary_apply_url(self):
        """
        Strict Apply button priority:
        1. official_application_url
        2. application_url
        3. notification_url
        4. official_website
        """
        return self.official_application_url or self.application_url or self.notification_url or self.official_website