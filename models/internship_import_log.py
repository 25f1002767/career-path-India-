from datetime import datetime
from extensions import db


class InternshipImportLog(db.Model):
    """
    Audit log for bulk import operations (CSV/JSON/API).
    Tracks detected, new, updated, duplicate, invalid, and failed records.
    """
    __tablename__ = "internship_import_logs"

    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(150), nullable=False)
    file_name = db.Column(db.String(255), nullable=True)
    is_dry_run = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default="COMPLETED")
    # STARTED, COMPLETED, FAILED, PARTIAL

    records_found = db.Column(db.Integer, default=0)
    created_count = db.Column(db.Integer, default=0)
    updated_count = db.Column(db.Integer, default=0)
    duplicate_count = db.Column(db.Integer, default=0)
    invalid_count = db.Column(db.Integer, default=0)
    failed_count = db.Column(db.Integer, default=0)

    error_summary = db.Column(db.Text, nullable=True)
    log_details = db.Column(db.Text, nullable=True)

    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
