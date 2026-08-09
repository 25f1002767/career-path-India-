from flask import (
    Blueprint,
    render_template,
    request,
    abort
)

from services.knowledge.career_service import (
    career_service
)

from services.skill_gap import (
    analyze_skill_gap
)

career = Blueprint(
    "career",
    __name__,
    url_prefix="/careers"
)

# ==========================================
# Career List
# ==========================================

@career.route("/")
def career_list():

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    careers = career_service.search(
        keyword=search,
        category=category
    )

    categories = career_service.categories()

    return render_template(
        "career/list.html",
        careers=careers,
        categories=categories,
        search=search,
        selected_category=category
    )

# ==========================================
# Career Details
# ==========================================

@career.route("/<slug>")
def career_detail(slug):

    career_data = career_service.get_by_slug(slug)

    if career_data is None:
        abort(404)

    # Related careers
    related = [

        c for c in career_service.get_all()

        if c["category"] == career_data["category"]

        and c["slug"] != slug

    ][:3]

    # Demo user skills
    user_skills = [

        "Python",
        "Communication"

    ]

    # Skill gap analysis
    gap = analyze_skill_gap(
        career_data,
        user_skills
    )

    return render_template(
        "career/details.html",
        career=career_data,
        related=related,
        gap=gap
    )

# ==========================================
# Compare Careers
# ==========================================

@career.route("/compare")
def compare():

    slug1 = request.args.get("career1")
    slug2 = request.args.get("career2")

    careers = career_service.get_all()

    if not slug1 or not slug2:

        return render_template(
            "career/compare_select.html",
            careers=careers
        )

    career1 = career_service.get_by_slug(slug1)
    career2 = career_service.get_by_slug(slug2)

    if career1 is None or career2 is None:
        abort(404)

    return render_template(
        "career/compare.html",
        career1=career1,
        career2=career2
    )