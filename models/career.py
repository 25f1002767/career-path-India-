from datetime import datetime
import json
from extensions import db


class Career(db.Model):
    """
    Comprehensive National Career Discovery Model.
    Aligned with National Career Service (NCS), National Classification of Occupations (NCO),
    and Sector Skill Councils (SSC) standards.
    """
    __tablename__ = "careers"

    id = db.Column(db.Integer, primary_key=True)

    # ==========================================
    # Basic Identification & Classification
    # ==========================================
    title = db.Column(db.String(150), nullable=False, index=True)
    short_name = db.Column(db.String(100), nullable=True, index=True)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    sub_category = db.Column(db.String(100), nullable=True, index=True)
    industry = db.Column(db.String(100), nullable=True, index=True)
    icon = db.Column(db.String(100), default="briefcase")

    # ==========================================
    # Detailed Descriptions & Day-to-Day
    # ==========================================
    short_description = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=False)
    what_they_do = db.Column(db.Text, nullable=True)
    day_to_day_work = db.Column(db.Text, nullable=True)
    work_environment = db.Column(db.String(150), nullable=True)
    work_modes = db.Column(db.String(150), default="On-site / Hybrid")  # On-site, Hybrid, Remote, Field Work

    # ==========================================
    # Academic & Eligibility Foundations
    # ==========================================
    education_required = db.Column(db.String(255), nullable=True)
    minimum_qualification = db.Column(db.String(100), default="Undergraduate", index=True)  # Class 10, Class 12, Diploma, Undergraduate, Postgraduate
    preferred_streams = db.Column(db.String(255), nullable=True)  # Science (PCM), Science (PCB), Commerce, Arts, Any Stream
    required_subjects = db.Column(db.String(255), nullable=True)

    # ==========================================
    # Structured Skills & Tools
    # ==========================================
    skills_required = db.Column(db.Text, nullable=True)  # Legacy string
    technical_skills = db.Column(db.Text, nullable=True)
    soft_skills = db.Column(db.Text, nullable=True)
    tools = db.Column(db.Text, nullable=True)
    certifications = db.Column(db.Text, nullable=True)

    # ==========================================
    # Progression, Pathways & Experience
    # ==========================================
    experience_level = db.Column(db.String(50), default="Entry-Level to Mid-Level")
    career_growth = db.Column(db.String(255), nullable=True)
    career_progression = db.Column(db.Text, nullable=True)  # Structured JSON or text ladder
    entry_routes = db.Column(db.Text, nullable=True)  # Path A: Common, Path B: Alternative, Path C: Specialized
    higher_study_options = db.Column(db.Text, nullable=True)
    entrepreneurship_options = db.Column(db.Text, nullable=True)
    internship_roles = db.Column(db.Text, nullable=True)
    entry_level_roles = db.Column(db.Text, nullable=True)

    # ==========================================
    # Sector Opportunities & Salary Transparency
    # ==========================================
    government_opportunities = db.Column(db.Text, nullable=True)
    private_opportunities = db.Column(db.Text, nullable=True)
    average_salary = db.Column(db.String(100), nullable=True)
    salary_indicative = db.Column(db.Text, nullable=True)  # Detailed indicative breakdown with provenance and non-guaranteed notice
    future_scope = db.Column(db.String(100), default="High Demand")

    # ==========================================
    # Legacy / Direct Cache fields
    # ==========================================
    entrance_exams = db.Column(db.Text, nullable=True)
    top_colleges = db.Column(db.Text, nullable=True)
    top_companies = db.Column(db.Text, nullable=True)
    roadmap_summary = db.Column(db.Text, nullable=True)
    projects_to_build = db.Column(db.Text, nullable=True)
    ai_prompt = db.Column(db.Text, nullable=True)

    # ==========================================
    # Balanced Universe & Discovery Dimensions
    # ==========================================
    is_lesser_known = db.Column(db.Boolean, default=False, index=True)
    career_family = db.Column(db.String(100), nullable=True, index=True)
    interest_clusters = db.Column(db.String(255), nullable=True)
    work_style = db.Column(db.String(255), nullable=True)
    reality_check = db.Column(db.Text, nullable=True)
    next_steps = db.Column(db.Text, nullable=True)

    # ==========================================
    # Source Provenance & Data Quality
    # ==========================================
    source = db.Column(db.String(255), default="National Career Service (NCS) / Sector Skill Councils")
    official_url = db.Column(db.String(350), nullable=True)
    verification_status = db.Column(db.String(50), default="VERIFIED", index=True)  # VERIFIED, NEEDS_REVIEW, ARCHIVED
    last_verified_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ==========================================
    # Relationships
    # ==========================================
    learning_progress = db.relationship(
        "LearningProgress",
        back_populates="career",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # Helper properties for UI
    @property
    def is_verified(self):
        return self.verification_status == "VERIFIED"

    @property
    def technical_skills_list(self):
        if self.technical_skills:
            return [s.strip() for s in self.technical_skills.split(",") if s.strip()]
        if self.skills_required:
            return [s.strip() for s in self.skills_required.split(",") if s.strip()]
        return []

    @property
    def soft_skills_list(self):
        if not self.soft_skills:
            return []
        return [s.strip() for s in self.soft_skills.split(",") if s.strip()]

    @property
    def tools_list(self):
        if not self.tools:
            return []
        return [s.strip() for s in self.tools.split(",") if s.strip()]

    @property
    def work_modes_list(self):
        if not self.work_modes:
            return ["On-site"]
        return [m.strip() for m in self.work_modes.split("/") if m.strip()]

    @property
    def preferred_streams_list(self):
        if not self.preferred_streams:
            return []
        return [s.strip() for s in self.preferred_streams.split(",") if s.strip()]

    @property
    def internship_roles_list(self):
        if not self.internship_roles:
            return []
        return [r.strip() for r in self.internship_roles.split(",") if r.strip()]

    @property
    def entry_level_roles_list(self):
        if not self.entry_level_roles:
            return []
        return [r.strip() for r in self.entry_level_roles.split(",") if r.strip()]

    @property
    def certifications_list(self):
        if not self.certifications:
            return []
        return [c.strip() for c in self.certifications.split(",") if c.strip()]

    @property
    def parsed_entry_routes(self):
        """Parse structured entry routes JSON or fallback to text"""
        if not self.entry_routes:
            return []
        try:
            return json.loads(self.entry_routes)
        except Exception:
            # Fallback to lines
            routes = []
            for line in self.entry_routes.split("\n"):
                line = line.strip()
                if line:
                    routes.append({"title": "Route Option", "description": line})
            return routes

    @property
    def parsed_career_progression(self):
        """Parse career ladder progression"""
        if not self.career_progression:
            return []
        try:
            return json.loads(self.career_progression)
        except Exception:
            ladder = []
            for step in self.career_progression.split("->"):
                if step.strip():
                    ladder.append({"stage": step.strip()})
            return ladder

    @property
    def is_without_coding(self):
        """Returns True if the career does not involve programming as a primary requirement"""
        cat = (self.category or "").lower()
        if "technology" in cat:
            return False
        tech_skills = (self.technical_skills or "").lower()
        coding_keywords = ["python", "java", "c++", "javascript", "coding", "software engineering", "algorithms"]
        return not any(k in tech_skills for k in coding_keywords)

    @property
    def is_without_engineering(self):
        """Returns True if the career does not require a formal engineering degree"""
        cat = (self.category or "").lower()
        title = (self.title or "").lower()
        edu = (self.minimum_qualification or "").lower()
        if "engineering & manufacturing" in cat:
            return False
        if "engineer" in title and "b.tech" in edu:
            return False
        return True

    @property
    def interest_clusters_list(self):
        if self.interest_clusters:
            return [c.strip() for c in self.interest_clusters.split(",") if c.strip()]
        # Fallback to deriving from category
        cat = self.category or ""
        clusters = []
        if any(k in cat for k in ["Healthcare", "Medical"]):
            clusters.extend(["People", "Helping", "Healthcare", "Science"])
        elif any(k in cat for k in ["Law", "Legal"]):
            clusters.extend(["Law", "Government", "Society", "Writing"])
        elif any(k in cat for k in ["Government", "Defence"]):
            clusters.extend(["Government", "Leadership", "Public Service", "Society"])
        elif any(k in cat for k in ["Finance", "Accounting"]):
            clusters.extend(["Numbers", "Business", "Analysis"])
        elif any(k in cat for k in ["Education", "Teaching"]):
            clusters.extend(["Teaching", "People", "Helping", "Language"])
        elif any(k in cat for k in ["Arts", "Humanities", "Social"]):
            clusters.extend(["Culture", "History", "Language", "Writing", "Society"])
        elif any(k in cat for k in ["Agriculture", "Environment"]):
            clusters.extend(["Nature", "Science", "Outdoor", "Hands-on"])
        elif any(k in cat for k in ["Creative", "Design", "Media"]):
            clusters.extend(["Creativity", "Art", "Design", "Communication"])
        elif any(k in cat for k in ["Sports", "Fitness"]):
            clusters.extend(["Sports", "Outdoor", "Health", "Hands-on"])
        elif any(k in cat for k in ["Hospitality", "Tourism"]):
            clusters.extend(["Travel", "People", "Food", "Service"])
        elif any(k in cat for k in ["Aviation", "Logistics", "Maritime"]):
            clusters.extend(["Travel", "Machines", "Logistics", "Operations"])
        elif any(k in cat for k in ["Skilled", "Trades", "Vocational"]):
            clusters.extend(["Hands-on", "Machines", "Practical", "Trades"])
        else:
            clusters.extend(["General", "Professional"])
        return clusters

    @property
    def work_style_list(self):
        if self.work_style:
            return [s.strip() for s in self.work_style.split(",") if s.strip()]
        if self.work_modes:
            return [m.strip() for m in self.work_modes.split("/") if m.strip()]
        return ["Office"]

    @property
    def parsed_next_steps(self):
        if self.next_steps:
            try:
                return json.loads(self.next_steps)
            except Exception:
                return [s.strip() for s in self.next_steps.split("\n") if s.strip()]
        # Context-aware default 3 steps
        cat = (self.category or "").lower()
        if "government" in cat or "defence" in cat:
            return [
                "Verify specific age eligibility, physical standards, and notification calendars on official portals.",
                "Review the preliminary & mains examination syllabus and begin regular reading of national newspapers and NCERT foundation texts.",
                "Engage in structured mock testing and physical training for physical tests where applicable."
            ]
        elif "healthcare" in cat or "medical" in cat:
            return [
                "Confirm that you meet compulsory subject criteria (Physics, Chemistry, Biology) in Class 12.",
                "Prepare for the relevant national entrance exam (e.g. NEET-UG, INI-CET, or State Allied Health CETs).",
                "Explore MCI/NMC/DCI/PCI recognized teaching hospitals and research medical colleges."
            ]
        elif any(k in cat for k in ["design", "creative", "media", "fine arts", "performing"]):
            return [
                "Begin cultivating your personal creative portfolio, sketchbook, writing samples, or performance recordings.",
                "Prepare for aptitude and creative design examinations (e.g. NID DAT, UCEED, NIFT, or university media auditions).",
                "Seek freelance projects, student festivals, or internships to build real-world credibility."
            ]
        elif "law" in cat:
            return [
                "Read legal reasoning, constitutional basics, and current affairs regularly.",
                "Prepare for CLAT, AILET, or university law entrance tests for 5-year integrated BA LLB / BBA LLB.",
                "Participate in debate competitions and seek judicial or chamber shadowing internships."
            ]
        else:
            return [
                f"Explore recognized degree options linked to {self.title} on MPath.",
                "Check institutions offering relevant programs and evaluate curriculum and industry exposure.",
                "Start learning foundational skills and seek hands-on projects or internships."
            ]

    @property
    def reality_check_points(self):
        if self.reality_check:
            return [p.strip() for p in self.reality_check.split("\n") if p.strip()]
        # Default realistic observations
        cat = (self.category or "").lower()
        if "government" in cat:
            return [
                "Competition ratio is high (often under 0.5% final selection); maintaining alternate career backups is prudent.",
                "Posting locations can involve rural or hardship areas during initial service tenures.",
                "Preparation requires 1-2 years of disciplined, consistent study."
            ]
        elif "medical" in cat or "healthcare" in cat:
            return [
                "Education period is long (5.5 to 8+ years including compulsory internships and post-graduate residency).",
                "Demands emotional resilience, patient empathy, and emergency night duty shifts.",
                "Requires mandatory statutory registration with National/State Medical, Dental, or Allied Health Councils."
            ]
        elif any(k in cat for k in ["creative", "film", "performing", "fine arts"]):
            return [
                "Early career income may be project-based or variable before establishing a strong client or studio reputation.",
                "Portfolio quality, uniqueness of vision, and networking matter far more than academic marks alone.",
                "Continuous practice and willingness to receive critical artistic feedback are essential."
            ]
        elif "law" in cat:
            return [
                "Court litigation requires several years of apprenticeship under senior advocates before establishing independent practice.",
                "Corporate law demands long analytical reading hours and high attention to detail in contracts.",
                "Clearing the All India Bar Examination (AIBE) is mandatory to practice before Indian courts."
            ]
        else:
            return [
                "Entry salary scales are indicative and depend on candidate aptitude, college reputation, and performance.",
                "Continuous upskilling and professional certifications are required throughout your career.",
                "Building early practical internship experience significantly accelerates job placement."
            ]

    def __repr__(self):
        return f"<Career {self.title} ({self.category}) - {self.verification_status}>"