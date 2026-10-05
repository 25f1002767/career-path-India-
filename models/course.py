from extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True, index=True)
    short_name = db.Column(db.String(50), nullable=True, index=True)
    level = db.Column(db.String(50), nullable=True, index=True)  # Diploma, UG, PG, PhD, Certificate, Integrated
    discipline = db.Column(db.String(100), nullable=True, index=True)  # Science, Engineering, Medical, Commerce, Management, Arts & Humanities, Law, Design, Education
    stream = db.Column(db.String(100), nullable=True)  # Science (PCM), Science (PCB), Commerce, Arts, Any Stream
    duration = db.Column(db.String(50), nullable=True)  # 3 Years, 4 Years, 2 Years, etc.
    description = db.Column(db.Text, nullable=True)
    aliases = db.Column(db.String(350), nullable=True, index=True)  # Comma-separated search aliases
    specialization = db.Column(db.String(200), nullable=True)
    eligibility_summary = db.Column(db.String(300), nullable=True)
    admission_modes = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship to CollegeCourse
    college_courses = db.relationship(
        "CollegeCourse",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    @property
    def alias_list(self):
        if not self.aliases:
            return []
        return [a.strip() for a in self.aliases.split(",") if a.strip()]

    @property
    def institution_count(self):
        return self.college_courses.filter_by(verification_status="VERIFIED").count()

    def __repr__(self):
        return f"<Course {self.name} ({self.level})>"


class CollegeCourse(db.Model):
    __tablename__ = "college_courses"

    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(
        db.Integer,
        db.ForeignKey("colleges.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Program-level precision
    program_name = db.Column(db.String(250), nullable=True)  # e.g. "B.Sc (Hons.) Mathematics"
    degree = db.Column(db.String(100), nullable=True)  # e.g. "Bachelor of Science"
    level = db.Column(db.String(50), nullable=True, index=True)  # UG, PG, PhD, Diploma, Integrated
    duration = db.Column(db.String(50), nullable=True)
    mode = db.Column(db.String(50), default="Regular", nullable=True)  # Regular, Distance, Online
    specialization = db.Column(db.String(150), nullable=True)
    
    # Admission & Seats
    eligibility = db.Column(db.String(255), nullable=True)
    admission_mode = db.Column(db.String(120), nullable=True)  # CUET-UG, JEE Main, NEET-UG, Merit-Based, etc.
    entrance_exam = db.Column(db.String(150), nullable=True)
    seats = db.Column(db.Integer, nullable=True)  # Official intake capacity from AISHE
    fees_approx = db.Column(db.String(100), nullable=True)
    academic_year = db.Column(db.String(20), nullable=True)  # e.g. "2024"
    
    # Source & Verification
    source = db.Column(db.String(255), default="Ministry of Education - AISHE Registry")
    source_url = db.Column(db.String(350), nullable=True)
    verification_status = db.Column(db.String(50), default="VERIFIED", index=True)  # VERIFIED, NEEDS_REVIEW, ARCHIVED
    last_verified_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    college = db.relationship("College", back_populates="college_courses")
    course = db.relationship("Course", back_populates="college_courses")

    @property
    def display_program_name(self):
        return self.program_name or (self.course.name if self.course else "Program")

    @property
    def is_verified(self):
        return self.verification_status == "VERIFIED"

    def __repr__(self):
        return f"<CollegeCourse College:{self.college_id} Course:{self.course_id} Program:{self.program_name}>"
