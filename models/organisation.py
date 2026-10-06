from datetime import datetime
from extensions import db
import re


def generate_slug(text: str) -> str:
    if not text:
        return ""
    slug = re.sub(r"[^\w\s-]", "", text.lower().strip())
    return re.sub(r"[-\s]+", "-", slug)


class Organisation(db.Model):
    """
    Normalized entity representing an employer, government body, ministry,
    university, or research institution offering internships.
    """
    __tablename__ = "organisations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    logo_url = db.Column(db.String(500), nullable=True)

    # Classification
    organisation_type = db.Column(db.String(100), default="Corporate", index=True)
    # Government, Ministry, Department, PSU, Corporate, MNC, Indian Company, Startup, MSME, NGO, University, Research Institute
    industry = db.Column(db.String(150), nullable=True, index=True)
    sector = db.Column(db.String(150), nullable=True, index=True)
    description = db.Column(db.Text, nullable=True)

    # Official Contact & Portals
    official_website = db.Column(db.String(500), nullable=True)
    official_contact_url = db.Column(db.String(500), nullable=True)

    # Location
    headquarters = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True, index=True)
    state = db.Column(db.String(100), nullable=True, index=True)
    country = db.Column(db.String(100), default="India")

    # Category Flags
    is_government = db.Column(db.Boolean, default=False, index=True)
    is_psu = db.Column(db.Boolean, default=False, index=True)
    is_corporate = db.Column(db.Boolean, default=True, index=True)
    is_startup = db.Column(db.Boolean, default=False, index=True)
    is_ngo = db.Column(db.Boolean, default=False, index=True)
    is_university = db.Column(db.Boolean, default=False, index=True)
    is_research = db.Column(db.Boolean, default=False, index=True)

    # Verification
    verified = db.Column(db.Boolean, default=True)
    verification_status = db.Column(db.String(50), default="VERIFIED_OFFICIAL", index=True)
    verification_source = db.Column(db.String(255), nullable=True)
    verification_date = db.Column(db.DateTime, default=datetime.utcnow)
    source_url = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    internships = db.relationship("Internship", backref="organisation", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug and self.name:
            self.slug = generate_slug(self.name)
        # Auto-compute category flags based on organisation_type
        t = (self.organisation_type or "").lower()
        if any(g in t for g in ["government", "ministry", "department"]):
            self.is_government = True
            self.is_corporate = False
        elif "psu" in t or "public sector" in t:
            self.is_psu = True
            self.is_government = True
            self.is_corporate = False
        elif "startup" in t:
            self.is_startup = True
        elif any(u in t for u in ["university", "college", "institute"]):
            self.is_university = True
            self.is_corporate = False
        elif "research" in t:
            self.is_research = True
            self.is_corporate = False
        elif "ngo" in t or "non-profit" in t:
            self.is_ngo = True
            self.is_corporate = False

    @property
    def active_internships_count(self):
        from models.internship import Internship
        return self.internships.filter(Internship.is_active.is_(True)).count()
