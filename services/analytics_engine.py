from models.user import User
from models.career import Career
from models.resume import Resume
from models.assessment import AssessmentResult
from models.saved_career import SavedCareer


def get_dashboard_stats():

    stats = {}

    stats["students"] = User.query.count()

    stats["careers"] = Career.query.count()

    stats["resumes"] = Resume.query.count()

    stats["assessments"] = AssessmentResult.query.count()

    stats["saved"] = SavedCareer.query.count()

    return stats