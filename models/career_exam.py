from extensions import db


class CareerExam(db.Model):
    """
    Relational mapping between Career and Government/Entrance/Competitive Exam.
    Connects Career -> Exam without duplicating exam details.
    """
    __tablename__ = "career_exams"

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("government_exams.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # PRIMARY, ALTERNATIVE, OPTIONAL, ELIGIBILITY, STATE_LEVEL
    importance = db.Column(db.String(50), default="PRIMARY", index=True)
    eligibility_summary = db.Column(db.String(255), nullable=True)
    verification_status = db.Column(db.String(50), default="VERIFIED", index=True)

    # Relationships
    career = db.relationship("Career", backref=db.backref("career_exams", lazy="select", cascade="all, delete-orphan"))
    exam = db.relationship("GovernmentExam", backref=db.backref("career_exams", lazy="select", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<CareerExam Career:{self.career_id} -> Exam:{self.exam_id} ({self.importance})>"
