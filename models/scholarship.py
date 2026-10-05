from extensions import db
import json
import urllib.parse
from datetime import datetime


def is_valid_http_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    u = url.strip()
    if not (u.startswith("http://") or u.startswith("https://")):
        return False
    lower = u.lower()
    if lower.startswith("javascript:") or lower.startswith("data:") or lower.startswith("file:"):
        return False
    if any(h in lower for h in ["localhost", "127.0.0.1", "0.0.0.0", "169.254.", "::1"]):
        return False
    if u in ["#", "/"]:
        return False
    try:
        parsed = urllib.parse.urlparse(u)
        hostname = (parsed.hostname or "").lower()
        if not hostname:
            return False
        if hostname in ["localhost", "test", "example.com"] or hostname.endswith(".local") or hostname.endswith(".internal"):
            return False
        return bool(parsed.netloc)
    except Exception:
        return False


class Scholarship(db.Model):
    __tablename__ = "scholarships"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, index=True)
    short_title = db.Column(db.String(150), nullable=True)

    provider = db.Column(db.String(200))
    provider_name = db.Column(db.String(250), nullable=True)
    provider_type = db.Column(db.String(100), default="Central Government", index=True)
    ministry = db.Column(db.String(250), nullable=True)
    department = db.Column(db.String(250), nullable=True)
    organization = db.Column(db.String(250), nullable=True)

    category = db.Column(db.String(100), index=True)
    sub_category = db.Column(db.String(150), nullable=True)
    scholarship_type = db.Column(db.String(100), default="Merit-cum-Means")

    national_or_state = db.Column(db.String(50), default="National")
    state = db.Column(db.String(100), nullable=True, index=True)
    district = db.Column(db.String(100), nullable=True)

    description = db.Column(db.Text)
    short_description = db.Column(db.Text, nullable=True)
    objective = db.Column(db.Text, nullable=True)

    education_level = db.Column(db.String(100), nullable=True, index=True)
    qualification = db.Column(db.String(150), nullable=True)
    minimum_qualification = db.Column(db.String(150), nullable=True)
    maximum_qualification = db.Column(db.String(150), nullable=True)

    streams = db.Column(db.String(255), nullable=True)
    courses = db.Column(db.Text, nullable=True)

    gender_eligibility = db.Column(db.String(50), default="All")
    age_min = db.Column(db.Integer, nullable=True)
    age_max = db.Column(db.Integer, nullable=True)

    family_income_limit = db.Column(db.Float, nullable=True)
    percentage_requirement = db.Column(db.Float, nullable=True)
    academic_requirement = db.Column(db.Text, nullable=True)
    eligibility = db.Column(db.Text)

    category_requirement = db.Column(db.String(100), default="All")
    disability_requirement = db.Column(db.String(50), default="None")
    domicile_requirement = db.Column(db.String(100), nullable=True)

    benefit_type = db.Column(db.String(100), default="Financial Support")
    amount = db.Column(db.String(100))
    amount_description = db.Column(db.Text, nullable=True)
    tuition_fee_support = db.Column(db.String(150), nullable=True)
    maintenance_allowance = db.Column(db.String(150), nullable=True)
    hostel_support = db.Column(db.String(150), nullable=True)
    book_allowance = db.Column(db.String(150), nullable=True)

    duration = db.Column(db.String(100), nullable=True)
    renewable = db.Column(db.Boolean, default=True)
    number_of_awards = db.Column(db.String(100), nullable=True)
    selection_process = db.Column(db.Text, nullable=True)

    deadline = db.Column(db.String(100))
    application_mode = db.Column(db.String(100), default="Online - National Scholarship Portal (NSP)")
    application_method = db.Column(db.String(50), default="EXTERNAL_PORTAL")

    official_website = db.Column(db.String(350), nullable=True)
    website = db.Column(db.String(255))
    official_url = db.Column(db.String(300), nullable=True)
    official_application_url = db.Column(db.String(350), nullable=True)
    notification_url = db.Column(db.String(350), nullable=True)
    guidelines_url = db.Column(db.String(350), nullable=True)
    faq_url = db.Column(db.String(350), nullable=True)

    application_url_status = db.Column(db.String(50), default="VALID", index=True)
    application_url_last_checked = db.Column(db.DateTime, nullable=True)
    application_url_verified_at = db.Column(db.DateTime, nullable=True)
    application_url_verified_by = db.Column(db.String(100), nullable=True)
    final_application_url = db.Column(db.String(350), nullable=True)

    requires_otr = db.Column(db.Boolean, default=False)
    requires_institute_verification = db.Column(db.Boolean, default=True)
    requires_nodal_verification = db.Column(db.Boolean, default=False)

    documents_required = db.Column(db.Text, nullable=True)
    common_mistakes = db.Column(db.Text, nullable=True)
    faqs = db.Column(db.Text, nullable=True)
    renewal_rules = db.Column(db.Text, nullable=True)

    source = db.Column(db.String(255), default="National & State Scholarship Portals")
    verification_status = db.Column(db.String(50), default="VERIFIED", index=True)
    last_verified_at = db.Column(db.DateTime, server_default=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Relationships
    cycles = db.relationship(
        "ScholarshipCycle",
        backref="scholarship",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="desc(ScholarshipCycle.academic_year)"
    )

    applications = db.relationship(
        "ScholarshipApplication",
        backref="scholarship",
        lazy=True,
        cascade="all, delete-orphan"
    )

    fields = db.relationship(
        "ScholarshipField",
        backref="scholarship",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="ScholarshipField.order"
    )

    @property
    def active_cycle(self):
        """Returns current open or latest cycle"""
        if not self.cycles:
            return None
        # Prefer OPEN or CLOSING_SOON
        for c in self.cycles:
            if c.status in ["OPEN", "CLOSING_SOON", "UPCOMING"]:
                return c
        return self.cycles[0]

    @property
    def resolved_application_url(self) -> str:
        """
        Cycle-aware application URL resolution.
        Priority:
        1. active_cycle.official_application_url (if valid and verified)
        2. self.official_application_url (if valid and verified)
        3. self.final_application_url (if valid and verified)
        Never blindly falls back to generic homepage or unverified URL!
        """
        if self.application_url_status in ["BROKEN", "MISSING", "ARCHIVED", "NEEDS_VERIFICATION", "HOMEPAGE_ONLY"]:
            if self.active_cycle and self.active_cycle.application_url_status in ["VALID", "REDIRECTED"] and is_valid_http_url(self.active_cycle.official_application_url):
                return self.active_cycle.official_application_url.strip()
            return None

        if self.active_cycle and is_valid_http_url(self.active_cycle.official_application_url):
            return self.active_cycle.official_application_url.strip()

        if is_valid_http_url(self.official_application_url):
            return self.official_application_url.strip()

        if is_valid_http_url(self.final_application_url):
            return self.final_application_url.strip()

        return None

    @property
    def resolved_official_website(self) -> str:
        """The organization or provider's main website"""
        for candidate in [self.official_website, self.official_url, self.website]:
            if is_valid_http_url(candidate):
                return candidate.strip()
        return "https://scholarships.gov.in"

    @property
    def is_homepage_as_app_url(self) -> bool:
        """
        Detects if the application URL is simply pointing to the root provider homepage.
        """
        app_url = self.official_application_url or self.resolved_application_url
        if not app_url:
            return False
        web_url = self.resolved_official_website

        if app_url.rstrip("/").lower() == web_url.rstrip("/").lower():
            return True

        try:
            p_app = urllib.parse.urlparse(app_url)
            p_web = urllib.parse.urlparse(web_url)
            if p_app.netloc.lower() == p_web.netloc.lower():
                path = (p_app.path or "").strip("/")
                if not path and not p_app.query:
                    return True
        except Exception:
            pass
        return False

    @property
    def homepage_duplication_warning(self) -> str:
        if self.is_homepage_as_app_url:
            return "Possible homepage/application URL duplication"
        return ""

    @property
    def has_direct_apply(self) -> bool:
        """True if there is an active, valid, non-broken application URL"""
        if self.application_url_status in ["BROKEN", "MISSING", "ARCHIVED", "NEEDS_VERIFICATION", "HOMEPAGE_ONLY"]:
            return False
        url = self.resolved_application_url
        return bool(url and is_valid_http_url(url))

    @property
    def apply_button_meta(self) -> dict:
        """
        Returns structured metadata for rendering the Apply button across all templates.
        Enforces deadline awareness and URL availability.
        """
        cycle = self.active_cycle
        cycle_status = (cycle.status if cycle else "OPEN") or "OPEN"

        if cycle_status == "CLOSED":
            return {
                "label": "Application Closed",
                "badge_class": "secondary",
                "is_enabled": False,
                "icon": "",
                "url": None,
                "reason": "The application window for the current cycle has closed."
            }

        if cycle_status == "UPCOMING":
            return {
                "label": f"Upcoming ({cycle.application_start_date or 'Soon'})",
                "badge_class": "info text-dark",
                "is_enabled": False,
                "icon": "",
                "url": None,
                "reason": "Application cycle will open as announced in the notification."
            }

        if not self.has_direct_apply:
            return {
                "label": "Application Link Unavailable",
                "badge_class": "warning text-dark",
                "is_enabled": False,
                "icon": "",
                "url": None,
                "reason": "Direct online application link is currently undergoing verification or only offline application is supported."
            }

        return {
            "label": "Apply Now",
            "badge_class": "primary",
            "is_enabled": True,
            "icon": "",
            "url": self.resolved_application_url,
            "reason": "Direct verified application portal available."
        }

    @property
    def source_url(self):
        return self.source or self.official_url

    @property
    def source_name(self):
        return self.provider or "Official Scholarship Portal"

    @property
    def parsed_documents(self):
        if not self.documents_required:
            return [
                "Income Certificate",
                "Domicile Certificate",
                "Previous Class Marksheet",
                "College Bonafide / Admission Receipt",
                "Aadhaar Card"
            ]
        try:
            if self.documents_required.strip().startswith("["):
                return json.loads(self.documents_required)
            return [d.strip() for d in self.documents_required.split(",") if d.strip()]
        except Exception:
            return [d.strip() for d in self.documents_required.split(",") if d.strip()]

    @property
    def parsed_faqs(self):
        if not self.faqs:
            return []
        try:
            return json.loads(self.faqs)
        except Exception:
            return []

    @property
    def parsed_mistakes(self):
        if not self.common_mistakes:
            return [
                "Mismatch between student name on Aadhaar and Class 10 Certificate.",
                "Submitting an expired Family Income Certificate.",
                "Delaying institute-level nodal officer verification after online submission.",
                "Entering an incorrect IFSC code or an inactive bank account."
            ]
        try:
            if self.common_mistakes.strip().startswith("["):
                return json.loads(self.common_mistakes)
            return [m.strip() for m in self.common_mistakes.split("\n") if m.strip()]
        except Exception:
            return [self.common_mistakes]

    @property
    def display_status(self):
        cyc = self.active_cycle
        st = cyc.status if cyc else "OPEN"
        status_map = {
            "OPEN": ("Applications Open", "success", ""),
            "CLOSING_SOON": ("Closing Soon", "warning text-dark", ""),
            "UPCOMING": ("Upcoming Cycle", "info text-dark", ""),
            "CLOSED": ("Applications Closed", "danger", ""),
            "NOTIFICATION_EXPECTED": ("Notification Expected", "secondary", ""),
            "ARCHIVED": ("Archived", "secondary", "")
        }
        return status_map.get(st, (st or "Open", "success", ""))

    def __repr__(self):
        return f"<Scholarship {self.id}: {self.title}>"


class ScholarshipCycle(db.Model):
    __tablename__ = "scholarship_cycles"

    id = db.Column(db.Integer, primary_key=True)
    scholarship_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarships.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    academic_year = db.Column(db.String(50), nullable=False)  # e.g. "2026-27"
    application_start_date = db.Column(db.String(50), nullable=True)
    application_end_date = db.Column(db.String(50), nullable=True)
    correction_start_date = db.Column(db.String(50), nullable=True)
    correction_end_date = db.Column(db.String(50), nullable=True)
    verification_deadline = db.Column(db.String(50), nullable=True)
    result_date = db.Column(db.String(50), nullable=True)
    disbursement_date = db.Column(db.String(50), nullable=True)

    status = db.Column(db.String(50), default="OPEN", index=True)
    amount = db.Column(db.String(100), nullable=True)
    vacancies_or_slots = db.Column(db.String(100), nullable=True)

    official_application_url = db.Column(db.String(350), nullable=True)
    official_website = db.Column(db.String(350), nullable=True)
    notification_url = db.Column(db.String(350), nullable=True)
    guidelines_url = db.Column(db.String(350), nullable=True)
    faq_url = db.Column(db.String(350), nullable=True)
    source_url = db.Column(db.String(350), nullable=True)
    application_url_status = db.Column(db.String(50), default="VALID")

    verification_status = db.Column(db.String(50), default="VERIFIED")
    last_verified_at = db.Column(db.DateTime, server_default=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    applications = db.relationship(
        "ScholarshipApplication",
        backref="cycle",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ScholarshipCycle {self.academic_year} for Sch:{self.scholarship_id}>"


class ScholarshipApplicationClick(db.Model):
    __tablename__ = "scholarship_application_clicks"

    id = db.Column(db.Integer, primary_key=True)
    scholarship_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarships.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    cycle_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarship_cycles.id", ondelete="SET NULL"),
        nullable=True
    )
    target_url = db.Column(db.String(500), nullable=False)
    click_source = db.Column(db.String(100), default="direct")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    scholarship = db.relationship("Scholarship", backref="outbound_clicks", lazy=True)

    def __repr__(self):
        return f"<ScholarshipClick Sch:{self.scholarship_id} Target:{self.target_url[:30]}>"


class ScholarshipApplication(db.Model):
    __tablename__ = "scholarship_applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    scholarship_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarships.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    cycle_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarship_cycles.id", ondelete="SET NULL"),
        nullable=True
    )

    application_number = db.Column(db.String(100), unique=True, index=True)
    external_reference_number = db.Column(db.String(100), nullable=True)

    status = db.Column(db.String(50), default="DRAFT", index=True)
    submission_type = db.Column(db.String(50), default="EXTERNAL_PORTAL_PREPARED")
    progress_percent = db.Column(db.Integer, default=15)

    form_data = db.Column(db.Text, nullable=True)  # JSON dictionary of form fields
    eligibility_snapshot = db.Column(db.Text, nullable=True)  # JSON snapshot of match results
    student_notes = db.Column(db.Text, nullable=True)

    user_declared_status = db.Column(db.String(50), nullable=True)
    user_declared_status_updated_at = db.Column(db.DateTime, nullable=True)

    submitted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Linked documents
    application_documents = db.relationship(
        "ScholarshipApplicationDocument",
        backref="application",
        lazy=True,
        cascade="all, delete-orphan"
    )

    @property
    def parsed_form_data(self):
        if not self.form_data:
            return {}
        try:
            return json.loads(self.form_data)
        except Exception:
            return {}

    @property
    def parsed_eligibility_snapshot(self):
        if not self.eligibility_snapshot:
            return {}
        try:
            return json.loads(self.eligibility_snapshot)
        except Exception:
            return {}

    @property
    def display_status_badge(self):
        status_badges = {
            "DRAFT": ("Draft (In Progress)", "secondary", ""),
            "PROFILE_INCOMPLETE": ("Profile Incomplete", "warning text-dark", ""),
            "ELIGIBILITY_CHECK": ("Eligibility Matched", "info text-dark", ""),
            "DOCUMENTS_PENDING": ("Documents Pending", "warning text-dark", ""),
            "READY_TO_SUBMIT": ("Ready to Submit", "primary", ""),
            "SUBMITTED": ("Portal Submission Initiated", "primary", ""),
            "INSTITUTE_VERIFICATION": ("Institute Verification Pending", "info text-dark", ""),
            "DEPARTMENT_VERIFICATION": ("Department Review", "info text-dark", ""),
            "CORRECTION_REQUIRED": ("Correction Required", "danger", ""),
            "APPROVED": ("Approved", "success", ""),
            "REJECTED": ("Rejected", "danger", ""),
            "PAYMENT_PENDING": ("Payment / DBT Pending", "success bg-opacity-75", ""),
            "PAYMENT_RECEIVED": ("Disbursed / Received", "success", ""),
            "CLOSED": ("Closed", "secondary", "")
        }
        return status_badges.get(self.status, (self.status or "Active", "secondary", ""))

    def __repr__(self):
        return f"<ScholarshipApplication #{self.id} User:{self.user_id} Sch:{self.scholarship_id} ({self.status})>"


class ScholarshipField(db.Model):
    __tablename__ = "scholarship_fields"

    id = db.Column(db.Integer, primary_key=True)
    scholarship_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarships.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    field_name = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    field_type = db.Column(db.String(50), default="text")
    required = db.Column(db.Boolean, default=True)
    validation_rule = db.Column(db.String(100), nullable=True)
    options = db.Column(db.Text, nullable=True)
    help_text = db.Column(db.String(255), nullable=True)
    section = db.Column(db.String(50), default="ACADEMIC")
    order = db.Column(db.Integer, default=0)
    sensitive = db.Column(db.Boolean, default=False)
    autofill_source = db.Column(db.String(100), nullable=True)

    @property
    def parsed_options(self):
        if not self.options:
            return []
        return [o.strip() for o in self.options.split(",") if o.strip()]

    def __repr__(self):
        return f"<ScholarshipField {self.field_name} ({self.field_type})>"


class StudentDocument(db.Model):
    __tablename__ = "student_documents"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    document_type = db.Column(db.String(100), nullable=False)
    document_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(350), nullable=False)
    file_size = db.Column(db.Integer, default=0)
    mime_type = db.Column(db.String(100), nullable=True)
    verification_status = db.Column(db.String(50), default="UPLOADED")
    notes = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())

    @property
    def file_name(self):
        return self.document_name

    def __repr__(self):
        return f"<StudentDocument #{self.id} User:{self.user_id} {self.document_type}>"


class ScholarshipApplicationDocument(db.Model):
    __tablename__ = "scholarship_application_documents"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer,
        db.ForeignKey("scholarship_applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    document_id = db.Column(
        db.Integer,
        db.ForeignKey("student_documents.id", ondelete="SET NULL"),
        nullable=True
    )
    document_type = db.Column(db.String(100), nullable=False)
    document_label = db.Column(db.String(200), nullable=False)
    is_mandatory = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(50), default="PENDING")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    document = db.relationship("StudentDocument", backref="application_links")

    def __repr__(self):
        return f"<AppDoc App:{self.application_id} DocType:{self.document_type} Status:{self.status}>"