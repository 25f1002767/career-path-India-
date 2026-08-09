from services.knowledge.career_service import career_service


class AIRecommendationService:

    @staticmethod
    def recommend(category):

        careers = career_service.get_all()

        results = []

        for career in careers:

            if career["category"].lower() == category.lower():

                results.append({

                    "title": career["title"],

                    "match": 90,

                    "reason": [

                        "Matches your assessment category",

                        "Strong future growth",

                        "Good salary potential"

                    ]

                })

        return results[:5]