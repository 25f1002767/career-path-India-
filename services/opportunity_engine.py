from models.career import Career
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship

from services.matching_engine import AIMatchingEngine

from services.eligibility_engine import (
    is_career_eligible,
    is_exam_eligible,
    is_scholarship_eligible,
    is_internship_eligible
)


def discover_opportunities(profile):

    opportunities = []

    # ==========================================
    # Careers
    # ==========================================

    careers = Career.query.all()

    for career in careers:

        if is_career_eligible(profile, career):

            match = AIMatchingEngine.calculate(
                profile,
                career
            )

            opportunities.append({

                "type": "Career",

                "id": career.id,

                "title": career.title,

                "category": career.category,

                "description": career.description,

                "salary": career.average_salary,

                "future_scope": career.future_scope,

                "education": career.education_required,

                "details": career,

                "icon": "bi bi-briefcase-fill",

                "match": match["score"],

                "reasons": match["reasons"]

            })

    # ==========================================
    # Government Exams
    # ==========================================

    exams = GovernmentExam.query.all()

    for exam in exams:

        if is_exam_eligible(profile, exam):

            match = AIMatchingEngine.calculate(
                profile,
                exam
            )

            opportunities.append({

                "type": "Government Exam",

                "id": exam.id,

                "title": exam.exam_name,

                "category": exam.category,

                "description": exam.description,

                "salary": exam.salary,

                "future_scope": "",

                "education": exam.qualification,

                "details": exam,

                "icon": "bi bi-file-earmark-text-fill",

                "match": match["score"],

                "reasons": match["reasons"]

            })

    # ==========================================
    # Scholarships
    # ==========================================

    scholarships = Scholarship.query.all()

    for scholarship in scholarships:

        if is_scholarship_eligible(profile, scholarship):

            match = AIMatchingEngine.calculate(
                profile,
                scholarship
            )

            opportunities.append({

                "type": "Scholarship",

                "id": scholarship.id,

                "title": scholarship.title,

                "category": scholarship.category,

                "description": scholarship.description,

                "salary": scholarship.amount,

                "future_scope": "",

                "education": scholarship.eligibility,

                "details": scholarship,

                "icon": "bi bi-mortarboard-fill",

                "match": match["score"],

                "reasons": match["reasons"]

            })

    # ==========================================
    # Internships
    # ==========================================

    internships = Internship.query.all()

    for internship in internships:

        if is_internship_eligible(profile, internship):

            match = AIMatchingEngine.calculate(
                profile,
                internship
            )

            opportunities.append({

                "type": "Internship",

                "id": internship.id,

                "title": internship.title,

                "category": internship.mode,

                "description": internship.description,

                "salary": internship.stipend,

                "future_scope": internship.duration,

                "education": internship.eligibility,

                "details": internship,

                "icon": "bi bi-building-fill",

                "match": match["score"],

                "reasons": match["reasons"]

            })

    # ==========================================
    # Sort by AI Match
    # ==========================================

    opportunities.sort(
        key=lambda x: x["match"],
        reverse=True
    )

    return opportunities


def search_opportunities(
    profile,
    keyword=None,
    category=None,
    opportunity_type=None
):

    opportunities = discover_opportunities(
        profile
    )

    filtered = []

    for item in opportunities:

        if keyword:

            text = (
                item["title"] +
                " " +
                (item["description"] or "")
            ).lower()

            if keyword.lower() not in text:
                continue

        if category:

            if (
                item["category"] or ""
            ).lower() != category.lower():
                continue

        if opportunity_type:

            if (
                item["type"].lower()
                !=
                opportunity_type.lower()
            ):
                continue

        filtered.append(item)

    return filtered


def get_statistics(profile):

    opportunities = discover_opportunities(
        profile
    )

    stats = {

        "total": len(opportunities),

        "careers": 0,

        "exams": 0,

        "scholarships": 0,

        "internships": 0

    }

    for item in opportunities:

        if item["type"] == "Career":

            stats["careers"] += 1

        elif item["type"] == "Government Exam":

            stats["exams"] += 1

        elif item["type"] == "Scholarship":

            stats["scholarships"] += 1

        elif item["type"] == "Internship":

            stats["internships"] += 1

    return stats