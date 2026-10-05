from extensions import db


class CareerCourse(db.Model):
    """
    Relational mapping between Career and canonical Course.
    Supports multi-route discovery: Career -> Course -> CollegeCourse -> College.
    """
    __tablename__ = "career_courses"

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(
        db.Integer,
        db.ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # DIRECT, COMMON, ALTERNATIVE, SPECIALIZED, FOUNDATIONAL
    relationship_type = db.Column(db.String(50), default="COMMON", index=True)
    description = db.Column(db.String(255), nullable=True)
    source_url = db.Column(db.String(350), nullable=True)
    verification_status = db.Column(db.String(50), default="VERIFIED", index=True)

    # Relationships
    career = db.relationship("Career", backref=db.backref("career_courses", lazy="select", cascade="all, delete-orphan"))
    course = db.relationship("Course", backref=db.backref("career_courses", lazy="select", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<CareerCourse Career:{self.career_id} -> Course:{self.course_id} ({self.relationship_type})>"
