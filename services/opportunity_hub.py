from models.career import Career
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship
from models.college import College

from services.matching_engine import AIMatchingEngine


class OpportunityHub:

    @staticmethod
    def get_all(profile):

        opportunities = []

        # Careers
        for career in Career.query.all():

            match = AIMatchingEngine.calculate(
                profile,
                career
            )

            opportunities.append({

                "type": "Career",

                "title": career.title,

                "match": match["score"],

                "reason": match["reasons"],

                "object": career

            })

        # Exams
        for exam in GovernmentExam.query.all():

            match = AIMatchingEngine.calculate(
                profile,
                exam
            )

            opportunities.append({

                "type": "Government Exam",

                "title": exam.exam_name,

                "match": match["score"],

                "reason": match["reasons"],

                "object": exam

            })

        # Scholarships
        for scholarship in Scholarship.query.all():

            match = AIMatchingEngine.calculate(
                profile,
                scholarship
            )

            opportunities.append({

                "type": "Scholarship",

                "title": scholarship.title,

                "match": match["score"],

                "reason": match["reasons"],

                "object": scholarship

            })

        # Internships
        for internship in Internship.query.all():

            match = AIMatchingEngine.calculate(
                profile,
                internship
            )

            opportunities.append({

                "type": "Internship",

                "title": internship.title,

                "match": match["score"],

                "reason": match["reasons"],

                "object": internship

            })

        # Colleges
        for college in College.query.all():

            opportunities.append({

                "type": "College",

                "title": college.name,

                "match": 100,

                "reason": ["Recommended College"],

                "object": college

            })

        opportunities.sort(
            key=lambda x: x["match"],
            reverse=True
        )

        return opportunities