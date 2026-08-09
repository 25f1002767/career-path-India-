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

    if not profile:
        return redirect(url_for("profile.create_profile"))

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