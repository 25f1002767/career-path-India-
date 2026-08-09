from extensions import db


class GovernmentExam(db.Model):

    __tablename__ = "government_exams"

    id = db.Column(db.Integer, primary_key=True)

    exam_name = db.Column(db.String(200), nullable=False)

    category = db.Column(db.String(100))

    qualification = db.Column(db.String(200))

    age_limit = db.Column(db.String(100))

    exam_pattern = db.Column(db.Text)

    syllabus = db.Column(db.Text)

    official_website = db.Column(db.String(300))

    salary = db.Column(db.String(100))

    description = db.Column(db.Text)