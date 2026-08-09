from models.career import Career

from services.career_match_engine import (
    calculate_match_score
)


def recommend_best_careers(context):

    careers = Career.query.all()

    recommendations = []

    for career in careers:

        score, reasons = calculate_match_score(
            context,
            career
        )

        recommendations.append({

            "career": career,

            "score": score,

            "reasons": reasons

        })

    recommendations.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return recommendations[:10]