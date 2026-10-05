from datetime import datetime
import json
from extensions import db


class AssessmentResult(db.Model):
    """
    Career Assessment & Discovery Attempt Record.
    Stores multi-dimensional student profile vectors, top matches,
    unexpected career discoveries, trade-offs, and next actions.
    Maintains backward compatibility with legacy 'recommended_category'.
    """
    __tablename__ = "assessment_results"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Legacy & primary headline representation
    recommended_category = db.Column(
        db.String(100),
        nullable=False,
        default="Career Discovery"
    )

    assessment_version = db.Column(
        db.String(20),
        default="2.0.0",
        nullable=True
    )

    confidence_level = db.Column(
        db.String(50),
        default="HIGH_CONFIDENCE",
        nullable=True
    )

    summary_headline = db.Column(
        db.String(255),
        nullable=True
    )

    # Structured JSON payloads
    answers_json = db.Column(db.Text, nullable=True)
    profile_json = db.Column(db.Text, nullable=True)
    recommendations_json = db.Column(db.Text, nullable=True)
    unexpected_json = db.Column(db.Text, nullable=True)
    tradeoffs_json = db.Column(db.Text, nullable=True)
    actions_json = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        default=datetime.utcnow,
        index=True
    )

    # ==========================================
    # Helper JSON Properties
    # ==========================================

    @property
    def parsed_answers(self):
        if not self.answers_json:
            return {}
        try:
            return json.loads(self.answers_json)
        except Exception:
            return {}

    @property
    def parsed_profile(self):
        if not self.profile_json:
            return {}
        try:
            return json.loads(self.profile_json)
        except Exception:
            return {}

    @property
    def parsed_recommendations(self):
        if not self.recommendations_json:
            return []
        try:
            return json.loads(self.recommendations_json)
        except Exception:
            return []

    @property
    def parsed_unexpected(self):
        if not self.unexpected_json:
            return []
        try:
            return json.loads(self.unexpected_json)
        except Exception:
            return []

    @property
    def parsed_tradeoffs(self):
        if not self.tradeoffs_json:
            return []
        try:
            return json.loads(self.tradeoffs_json)
        except Exception:
            return []

    @property
    def parsed_actions(self):
        if not self.actions_json:
            return []
        try:
            return json.loads(self.actions_json)
        except Exception:
            return []

    def __repr__(self):
        return f"<AssessmentResult User:{self.user_id} Rec:{self.recommended_category} ({self.created_at})>"