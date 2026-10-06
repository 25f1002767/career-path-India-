from datetime import datetime
from extensions import db


class StudentInternshipTracker(db.Model):
    """
    Student-side personal application lifecycle tracking.
    Statuses: Saved, Interested, Planning to Apply, Applied, Shortlisted, Interview, Selected, Rejected, Completed, Withdrawn.
    """
    __tablename__ = "student_internship_trackers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id", ondelete="CASCADE"), nullable=False, index=True)

    status = db.Column(db.String(50), default="Planning to Apply", index=True)
    # Saved, Interested, Planning to Apply, Applied, Shortlisted, Interview, Selected, Rejected, Completed, Withdrawn
    application_number = db.Column(db.String(100), nullable=True)
    applied_date = db.Column(db.Date, nullable=True)
    interview_date = db.Column(db.Date, nullable=True)
    stipend_offered = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref=db.backref("internship_trackers", lazy="dynamic", cascade="all, delete-orphan"))
    internship = db.relationship("Internship", backref=db.backref("trackers", lazy="dynamic", cascade="all, delete-orphan"))


class SavedInternship(db.Model):
    """
    Direct bookmarking relationship for student internships.
    """
    __tablename__ = "saved_internships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("saved_internships", lazy="dynamic", cascade="all, delete-orphan"))
    internship = db.relationship("Internship", backref=db.backref("saved_by_users", lazy="dynamic", cascade="all, delete-orphan"))
