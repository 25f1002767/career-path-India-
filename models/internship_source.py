from datetime import datetime
from extensions import db


class InternshipSource(db.Model):
    """
    Registry for official statutory internship sources, government scheme portals,
    and institutional providers (e.g., AICTE, TULIP, Indian Army, NHAI, Corporate Portals).
    """
    __tablename__ = "internship_sources"

    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    source_code = db.Column(db.String(100), nullable=False, unique=True, index=True)
    source_type = db.Column(db.String(100), default="STATUTORY_PORTAL", index=True)
    # STATUTORY_PORTAL, GOVERNMENT_SCHEME, PSU_PORTAL, CORPORATE_CAREERS, RESEARCH_INSTITUTION, UNIVERSITY_CELL
    official_url = db.Column(db.String(500), nullable=False)
    data_access_method = db.Column(db.String(100), default="APPROVED_EXPORT_OR_FEED")
    # PUBLIC_EXPORT, GOVERNMENT_OPEN_DATA, MANUAL_VERIFIED, REST_API
    permission_status = db.Column(db.String(100), default="PUBLIC_METADATA_PERMITTED")
    frequency = db.Column(db.String(50), default="WEEKLY")
    parser_version = db.Column(db.String(50), default="1.0.0")

    is_active = db.Column(db.Boolean, default=True)
    health_status = db.Column(db.String(50), default="HEALTHY", index=True)
    # HEALTHY, DEGRADED, NEEDS_REVIEW, INACTIVE
    records_count = db.Column(db.Integer, default=0)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    last_successful_import = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    internships = db.relationship("Internship", backref="source_rel", lazy="dynamic")
