from flask import Blueprint, render_template, session, redirect, url_for, request

from models.student_profile import StudentProfile
from services.opportunity_engine import (
    discover_opportunities,
    search_opportunities,
    get_statistics
)

opportunity = Blueprint(
    "opportunity",
    __name__,
    url_prefix="/opportunities"
)


@opportunity.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    profile = StudentProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    keyword = request.args.get("keyword")
    category = request.args.get("category")
    opportunity_type = request.args.get("type")

    if keyword or category or opportunity_type:

        opportunities = search_opportunities(
            profile,
            keyword,
            category,
            opportunity_type
        )

    else:

        opportunities = discover_opportunities(profile)

    stats = get_statistics(profile)

    return render_template(
        "opportunity/index.html",
        opportunities=opportunities,
        stats=stats,
        keyword=keyword,
        category=category,
        opportunity_type=opportunity_type
    )


@opportunity.route("/details/<string:type>/<int:item_id>")
def details(type, item_id):
    """
    Backward-compatible canonical redirect to specific item details.
    """
    t = type.lower()
    if "career" in t:
        from models.career import Career
        c = Career.query.get(item_id)
        if c and c.slug:
            return redirect(url_for("career.career_detail", slug=c.slug))
        return redirect(url_for("career.career_list"))
    elif "exam" in t:
        return redirect(url_for("exam.exam_detail", exam_id=item_id))
    elif "scholarship" in t:
        return redirect(url_for("scholarship.scholarship_detail", identifier=item_id))
    elif "internship" in t:
        return redirect(url_for("internship.internship_list"))
    return redirect(url_for("opportunity.home"))