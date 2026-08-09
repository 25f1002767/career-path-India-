from flask import Blueprint, render_template, request, abort
from services.knowledge.college_service import college_service

college = Blueprint(
    "college",
    __name__,
    url_prefix="/colleges"
)


@college.route("/")
def college_list():

    search = request.args.get("search", "").strip().lower()
    qualification = request.args.get("qualification", "").strip().lower()
    stream = request.args.get("stream", "").strip().lower()
    college_type = request.args.get("college_type", "").strip().lower()
    state = request.args.get("state", "").strip().lower()

    colleges = college_service.get_all()

    # Search
    if search:

        colleges = [

            c for c in colleges

            if search in c.get("name", "").lower()

            or search in c.get("course", "").lower()

            or search in c.get("city", "").lower()

        ]

    # Only ONE filter active
    elif state:

        colleges = [

            c for c in colleges

            if state in c.get("state", "").lower()

        ]

    elif college_type:

        colleges = [

            c for c in colleges

            if college_type in c.get("course", "").lower()

        ]

    elif stream:

        stream_map = {

            "pcm": [
                "engineering",
                "technology",
                "computer"
            ],

            "pcb": [
                "medical",
                "nursing",
                "pharmacy"
            ],

            "commerce": [
                "commerce",
                "b.com",
                "management",
                "mba"
            ],

            "arts": [
                "arts",
                "humanities",
                "social science",
                "law"
            ]

        }

        keywords = stream_map.get(stream, [])

        colleges = [

            c for c in colleges

            if any(

                k in c.get("course", "").lower()

                for k in keywords

            )

        ]

    elif qualification:

        colleges = colleges   # keep all for now

    return render_template(
        "college/list.html",
        colleges=colleges
    )


@college.route("/<int:index>")
def college_detail(index):

    colleges = college_service.get_all()

    if index < 0 or index >= len(colleges):
        abort(404)

    return render_template(
        "college/detail.html",
        college=colleges[index]
    )