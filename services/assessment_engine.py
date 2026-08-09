from models.career import Career


class AssessmentEngine:

    @staticmethod
    def analyze(answers):

        scores = {

            "Technology": 0,
            "Medical": 0,
            "Business": 0,
            "Government": 0,
            "Creative": 0

        }

        for answer in answers:

            if answer in scores:

                scores[answer] += 5

        best = max(
            scores,
            key=scores.get
        )

        careers = Career.query.filter_by(
            category=best
        ).limit(5).all()

        return {

            "category": best,

            "score": scores[best],

            "careers": careers,

            "all_scores": scores

        }