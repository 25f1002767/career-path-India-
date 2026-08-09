from models.user import User
from models.resume import Resume
from models.assessment import AssessmentResult
from models.saved_career import SavedCareer


def build_digital_twin(user_id):

    user = User.query.get(user_id)

    assessment = AssessmentResult.query.filter_by(
        user_id=user_id
    ).order_by(
        AssessmentResult.id.desc()
    ).first()

    resume = Resume.query.filter_by(
        user_id=user_id
    ).order_by(
        Resume.created_at.desc()
    ).first()

    saved = SavedCareer.query.filter_by(
        user_id=user_id
    ).count()

    twin = {

        "student": user.username if user else "",

        "career_category":
        assessment.recommended_category
        if assessment else "",

        "resume_score":
        resume.score
        if resume else 0,

        "saved_careers":
        saved,

        "skills":
        resume.missing_skills
        if resume else ""

    }

    return twin