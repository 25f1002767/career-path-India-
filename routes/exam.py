from flask import Blueprint, render_template, request
from services.knowledge.exam_service import exam_service

exam = Blueprint(
    "exam",
    __name__,
    url_prefix="/exams"
)


@exam.route("/")
def exam_list():

    search = request.args.get("search", "").strip().lower()
    qualification = request.args.get("qualification", "").strip().lower()
    stream = request.args.get("stream", "").strip().lower()
    graduation = request.args.get("graduation", "").strip().lower()
    category = request.args.get("category", "").strip().lower()

    exams = exam_service.get_all()

    # ------------------------------------------------
    # Search works separately
    # ------------------------------------------------
    if search:

        exams = [

            e for e in exams

            if search in e.get("name", "").lower()

        ]

    # ------------------------------------------------
    # Only ONE filter at a time
    # Priority: Category > Stream > Graduation > Qualification
    # ------------------------------------------------

    elif category:

        exams = [

            e for e in exams

            if category in e.get("category", "").lower()

        ]

    elif stream:

        stream_map = {

            "pcm": [
                "engineering",
                "railway",
                "defence",
                "space",
                "technology"
            ],

            "pcb": [
                "medical",
                "nursing",
                "health"
            ],

            "commerce": [
                "banking",
                "finance",
                "insurance",
                "economics"
            ],

            "arts": [
                "civil services",
                "teaching",
                "police",
                "law",
                "administration"
            ]

        }

        keywords = stream_map.get(stream, [])

        exams = [

            e for e in exams

            if any(

                k in e.get("category", "").lower()

                for k in keywords

            )

        ]

    elif graduation:

        graduation_map = {

            "engineering": [
                "engineering",
                "technology",
                "space",
                "railway"
            ],

            "science": [
                "medical",
                "research",
                "science"
            ],

            "commerce": [
                "banking",
                "finance",
                "insurance"
            ],

            "arts": [
                "civil services",
                "teaching",
                "police"
            ],

            "law": [
                "law"
            ]

        }

        keywords = graduation_map.get(graduation, [])

        exams = [

            e for e in exams

            if any(

                k in e.get("category", "").lower()

                for k in keywords

            )

        ]

    elif qualification:

        exams = [

            e for e in exams

            if qualification in e.get("eligibility", "").lower()

        ]

    return render_template(
        "exam/list.html",
        exams=exams
    )