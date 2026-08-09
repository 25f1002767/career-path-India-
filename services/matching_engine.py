from models.student_profile import StudentProfile


class AIMatchingEngine:

    @staticmethod
    def calculate(profile, opportunity):

        score = 0
        reasons = []

        # -----------------------------
        # Education Match (30)
        # -----------------------------

        education = ""

        if hasattr(opportunity, "education_required"):
            education = opportunity.education_required or ""

        elif hasattr(opportunity, "qualification"):
            education = opportunity.qualification or ""

        elif hasattr(opportunity, "eligibility"):
            education = opportunity.eligibility or ""

        if profile.current_class:

            if profile.current_class.lower() in education.lower():

                score += 30

                reasons.append(
                    "Education matches eligibility."
                )

        # -----------------------------
        # Career Goal (25)
        # -----------------------------

        title = ""

        if hasattr(opportunity, "title"):

            title = opportunity.title

        elif hasattr(opportunity, "exam_name"):

            title = opportunity.exam_name

        if profile.career_goal:

            if profile.career_goal.lower() in title.lower():

                score += 25

                reasons.append(
                    "Career goal matches."
                )

        # -----------------------------
        # Interests (20)
        # -----------------------------

        category = ""

        if hasattr(opportunity, "category"):

            category = opportunity.category or ""

        if profile.interests:

            interests = profile.interests.lower()

            if category.lower() in interests:

                score += 20

                reasons.append(
                    "Interest matches."
                )

        # -----------------------------
        # Strengths (15)
        # -----------------------------

        if hasattr(opportunity, "skills_required"):

            skills = opportunity.skills_required or ""

            if profile.strengths:

                for skill in profile.strengths.split(","):

                    if skill.strip().lower() in skills.lower():

                        score += 5

        # -----------------------------
        # State Bonus (10)
        # -----------------------------

        if hasattr(opportunity, "location"):

            if opportunity.location:

                if profile.state.lower() in opportunity.location.lower():

                    score += 10

                    reasons.append(
                        "Opportunity available in your state."
                    )

        score = min(score, 100)

        return {

            "score": score,

            "reasons": reasons

        }