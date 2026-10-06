from datetime import datetime
from extensions import db


class StudentOpportunityTracker(db.Model):
    """
    Personal student application tracking and reminders for opportunities and exam cycles.
    Tracks status: Interested, Planning to Apply, Applied, Admit Card Available, Exam Completed,
    Result Awaited, Qualified, Not Qualified, Selected.
    """
    __tablename__ = "student_opportunity_trackers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("government_exams.id", ondelete="CASCADE"), nullable=False, index=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey("exam_cycles.id", ondelete="SET NULL"), nullable=True, index=True)

    status = db.Column(db.String(50), default="Interested", index=True)
    # Interested, Planning to Apply, Applied, Admit Card Available, Exam Completed, Result Awaited, Qualified, Not Qualified, Selected
    application_number = db.Column(db.String(100), nullable=True)
    target_score = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    reminder_date = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OpportunityChangeLog(db.Model):
    """
    Audit log for changes in critical dates, vacancies, eligibility, and links
    discovered from official statutory updates.
    """
    __tablename__ = "opportunity_change_logs"

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey("government_exams.id", ondelete="CASCADE"), nullable=False, index=True)
    cycle_id = db.Column(db.Integer, nullable=True)
    field_name = db.Column(db.String(100), nullable=False)
    old_value = db.Column(db.Text, nullable=True)
    new_value = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(255), nullable=True)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
