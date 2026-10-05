from extensions import db


class College(db.Model):
    __tablename__ = "colleges"

    id = db.Column(db.Integer, primary_key=True)

    # Basic Identification
    aishe_code = db.Column(db.String(50), nullable=True, unique=True, index=True)
    name = db.Column(db.String(250), nullable=False, index=True)
    short_name = db.Column(db.String(80), nullable=True, index=True)

    # Classification & Hierarchy
    institution_type = db.Column(db.String(100), index=True)  # Central University, State Public University, IIT, NIT, AIIMS, Autonomous College, Affiliated College, etc.
    management_type = db.Column(db.String(100), nullable=True)  # Central Government, State Government, Private Un-Aided, etc.
    ownership = db.Column(db.String(100), nullable=True)
    institution_category = db.Column(db.String(60), index=True, default="College")  # University, College, Institute, Standalone
    university_name = db.Column(db.String(200), nullable=True)  # For universities, own name; for colleges, affiliating university
    affiliated_university = db.Column(db.String(200), nullable=True)  # Specific affiliating university

    # Location & Jurisdiction
    address = db.Column(db.String(350), nullable=True)
    city = db.Column(db.String(100), index=True)
    district = db.Column(db.String(100), index=True)
    state = db.Column(db.String(100), index=True)
    pincode = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Governance & Structure
    government_private = db.Column(db.String(50), index=True, default="Government")  # Government, Private, Aided, Unaided
    aided_unaided = db.Column(db.String(50), nullable=True)
    autonomous = db.Column(db.Boolean, default=False)
    established_year = db.Column(db.Integer, nullable=True)

    # Overview & Academics
    description = db.Column(db.Text, nullable=True)
    course = db.Column(db.String(350), nullable=True)  # Flat legacy text for fast fallback
    college_type = db.Column(db.String(100), nullable=True)  # Legacy column preserved

    # Financial & Outcomes (Legacy/Approx)
    fees = db.Column(db.String(100), nullable=True)
    placement = db.Column(db.String(100), nullable=True)
    highest_package = db.Column(db.String(100), nullable=True)
    average_package = db.Column(db.String(100), nullable=True)

    # Official Portals & Contact Information
    official_website = db.Column(db.String(300), nullable=True)
    website = db.Column(db.String(255), nullable=True)  # Legacy column
    official_url = db.Column(db.String(300), nullable=True)  # Legacy column
    admission_url = db.Column(db.String(300), nullable=True)
    contact_url = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(100), nullable=True)

    # Statutory Recognition & Accreditations
    recognition_status = db.Column(db.String(150), nullable=True)  # e.g. "UGC Recognized", "AICTE Approved"
    ugc_status = db.Column(db.String(60), nullable=True)
    aicte_status = db.Column(db.String(60), nullable=True)
    accreditation = db.Column(db.String(100), nullable=True)  # e.g. "NAAC"
    accreditation_grade = db.Column(db.String(20), nullable=True)  # e.g. "A++", "A+", "A", "B++"

    # NIRF Data
    nirf_participation = db.Column(db.Boolean, default=False)
    nirf_category = db.Column(db.String(80), nullable=True)
    nirf_rank = db.Column(db.Integer, nullable=True)
    nirf_rank_year = db.Column(db.Integer, nullable=True)

    # Provenance & Audit Verification
    source = db.Column(db.String(255), default="Official Higher Education Authority")
    source_url = db.Column(db.String(350), nullable=True)
    verification_status = db.Column(db.String(50), default="VERIFIED", index=True)
    last_verified_at = db.Column(db.DateTime, server_default=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationship to CollegeCourse
    college_courses = db.relationship(
        "CollegeCourse",
        back_populates="college",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    # Backward Compatibility & Convenience Properties
    @property
    def display_website(self):
        return self.official_website or self.official_url or self.website

    @property
    def display_type(self):
        return self.institution_type or self.college_type or "Recognized Institution"

    @property
    def is_verified(self):
        return self.verification_status == "VERIFIED"

    def __repr__(self):
        return f"<College {self.name} ({self.city}, {self.state})>"