from flask import (
    Blueprint,
    render_template,
    request
)

from services.knowledge.scholarship_service import (
    scholarship_service
)

scholarship = Blueprint(
    "scholarship",
    __name__,
    url_prefix="/scholarships"
)


@scholarship.route("/")
def scholarship_list():

    search = request.args.get(
        "search",
        ""
    )

    scholarships = scholarship_service.search(
        search
    )

    return render_template(

        "scholarship/list.html",

        scholarships=scholarships,

        search=search

    )