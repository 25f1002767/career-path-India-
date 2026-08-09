from models.career import Career


CATEGORY_REASONS = {
    "Technology": [
        "Strong logical thinking",
        "Excellent problem-solving ability",
        "Interest in technology and innovation"
    ],
    "Medical": [
        "Passion for helping people",
        "Scientific mindset",
        "Interest in healthcare"
    ],
    "Business": [
        "Leadership qualities",
        "Decision-making ability",
        "Business mindset"
    ],
    "Government": [
        "Public service mindset",
        "Leadership potential",
        "Social responsibility"
    ],
    "Creative": [
        "Creative thinking",
        "Innovation",
        "Design ability"
    ]
}


def calculate_match(category_score, total_score):

    if total_score == 0:
        return 0

    percentage = round(
        (category_score / total_score) * 100,
        1
    )

    return percentage


def recommend_careers(scores):

    total_score = sum(scores.values())

    recommendations = []

    careers = Career.query.all()

    for career in careers:

        category_score = scores.get(
            career.category,
            0
        )

        percentage = calculate_match(
            category_score,
            total_score
        )

        reasons = CATEGORY_REASONS.get(
            career.category,
            []
        )

        recommendations.append({

            "career": career,

            "percentage": percentage,

            "reasons": reasons,

            "skills": (
                career.skills_required.split(",")
                if career.skills_required
                else []
            ),

            "education": career.education_required,

            "salary": career.average_salary,

            "future": career.future_scope,

            "category": career.category

        })

    recommendations.sort(

        key=lambda x: (
            x["percentage"],
            x["future"] == "Excellent"
        ),

        reverse=True

    )

    return recommendations[:5]