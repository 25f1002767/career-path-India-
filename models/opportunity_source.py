from datetime import datetime
from extensions import db


class OpportunitySource(db.Model):
    """
    Registry for official statutory authorities, government directories,
    and verified recruitment boards across India.
    Supports Tier 1 (Official Authority), Tier 2 (Govt Directory), Tier 3 (Trusted Aggregator).
    """
    __tablename__ = "opportunity_sources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    organisation = db.Column(db.String(255), nullable=False, index=True)
    source_type = db.Column(db.String(100), default="Official Authority", index=True)
    authority_level = db.Column(db.String(50), default="TIER_1_OFFICIAL", index=True)
    # TIER_1_OFFICIAL, TIER_2_GOVERNMENT_DIRECTORY, TIER_3_TRUSTED_AGGREGATOR, OTHER
    base_url = db.Column(db.String(500), nullable=False)
    official = db.Column(db.Boolean, default=True)
    country = db.Column(db.String(100), default="India")
    state = db.Column(db.String(100), default="All India", index=True)
    category = db.Column(db.String(100), nullable=True, index=True)
    active = db.Column(db.Boolean, default=True)
    crawl_method = db.Column(db.String(100), default="STATUTORY_FEED")
    api_available = db.Column(db.Boolean, default=False)
    last_checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_success_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_failure_at = db.Column(db.DateTime, nullable=True)
    parser_version = db.Column(db.String(50), default="1.0.0")
    robots_checked = db.Column(db.Boolean, default=True)
    terms_review_status = db.Column(db.String(50), default="REVIEWED_PERMITTED")
    health_status = db.Column(db.String(50), default="HEALTHY", index=True)
    # HEALTHY, DEGRADED, NEEDS_REVIEW, INACTIVE
    records_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    exams = db.relationship("GovernmentExam", backref="source_rel", lazy="dynamic")
    cycles = db.relationship("ExamCycle", backref="source_rel", lazy="dynamic")

    @property
    def tier_badge(self):
        if self.authority_level == "TIER_1_OFFICIAL":
            return ("Tier 1: Official Authority", "success", "check-circle")
        elif self.authority_level == "TIER_2_GOVERNMENT_DIRECTORY":
            return ("Tier 2: Government Directory", "primary", "shield")
        elif self.authority_level == "TIER_3_TRUSTED_AGGREGATOR":
            return ("Tier 3: Aggregator (Discovery Only)", "warning text-dark", "search")
        return ("Standard Source", "secondary", "info")
