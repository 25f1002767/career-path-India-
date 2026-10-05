from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy import or_

from extensions import db
from models.internship import Internship
from models.saved_opportunity import SavedOpportunity

internship = Blueprint(
    "internship",
    __name__,
    url_prefix="/internships"
)


# ==========================================
# Internship List
# ==========================================

@internship.route("/")
def internship_list():
    search = request.args.get("search", "").strip()
    mode = request.args.get("mode", "").strip()
    domain = request.args.get("domain", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 12

    query = Internship.query

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Internship.title.ilike(pattern),
                Internship.company.ilike(pattern),
                Internship.skills.ilike(pattern),
                Internship.location.ilike(pattern),
                Internship.domain.ilike(pattern),
                Internship.description.ilike(pattern)
            )
        )

    if mode:
        query = query.filter(Internship.mode.ilike(f"%{mode}%"))

    if domain:
        query = query.filter(Internship.domain.ilike(f"%{domain}%"))

    query = query.order_by(Internship.id.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    internships = pagination.items

    # Distinct domains and modes for filters
    domains_raw = db.session.query(Internship.domain).distinct().all()
    domains = sorted([d[0] for d in domains_raw if d[0]])

    saved_internship_ids = set()
    if session.get("user_id"):
        user_saved = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="internship"
        ).all()
        saved_internship_ids = {s.item_id for s in user_saved}

    return render_template(
        "internship/list.html",
        internships=internships,
        pagination=pagination,
        domains=domains,
        search=search,
        selected_mode=mode,
        selected_domain=domain,
        saved_internship_ids=saved_internship_ids
    )


# ==========================================
# Bookmark Internship Toggle
# ==========================================

@internship.route("/save/<int:internship_id>")
def toggle_save(internship_id):
    if "user_id" not in session:
        flash("Please log in to save internships to your profile.", "info")
        return redirect(url_for("auth.login"))

    intern_obj = Internship.query.get_or_404(internship_id)

    existing = SavedOpportunity.query.filter_by(
        user_id=session["user_id"],
        opportunity_type="internship",
        item_id=internship_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f"{intern_obj.title} removed from saved internships.", "info")
    else:
        saved = SavedOpportunity(
            user_id=session["user_id"],
            opportunity_type="internship",
            item_id=internship_id,
            title=intern_obj.title
        )
        db.session.add(saved)
        db.session.commit()
        flash(f"{intern_obj.title} saved to your profile!", "success")

    return redirect(request.referrer or url_for("internship.internship_list"))