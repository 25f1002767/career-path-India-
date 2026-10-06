"""
National Internship Discovery Platform Blueprint.
Inspired by statutory Indian portal architectures (AICTE, MoHUA, Central Ministries).
Provides high-performance search, multi-faceted filtering, specialized hubs,
deterministic student matching, application tracking, and organization dossiers.
"""

from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from sqlalchemy import or_, and_, desc, asc

from extensions import db
from models.internship import Internship
from models.organisation import Organisation
from models.internship_source import InternshipSource
from models.internship_tracker import StudentInternshipTracker, SavedInternship
from models.saved_opportunity import SavedOpportunity
from models.user import User
from models.student_profile import StudentProfile
from models.career import Career
from models.course import Course
from models.college import College
from services.internship.matching_engine import InternshipMatchingEngine

internship = Blueprint(
    "internship",
    __name__,
    url_prefix="/internships"
)


# =========================================================================
# HELPER: BUILD FILTERED INTERNSHIP QUERY
# =========================================================================
def build_internship_query(args):
    search = args.get("search", "").strip()
    mode = args.get("mode", "").strip()
    category = args.get("category", "").strip() or args.get("domain", "").strip()
    org_type = args.get("org_type", "").strip()
    state = args.get("state", "").strip()
    city = args.get("city", "").strip()
    stipend_tier = args.get("stipend", "").strip()
    duration_tier = args.get("duration", "").strip()
    ppo = args.get("ppo", "").strip()
    credits = args.get("credits", "").strip()
    verified_only = args.get("verified", "").strip()
    sort_by = args.get("sort", "relevant").strip()

    query = Internship.query.filter(Internship.is_active == True)

    # 1. Full-text search
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Internship.title.ilike(pattern),
                Internship.organisation_name.ilike(pattern),
                Internship.scheme_name.ilike(pattern),
                Internship.category.ilike(pattern),
                Internship.skills.ilike(pattern),
                Internship.technical_skills.ilike(pattern),
                Internship.location.ilike(pattern),
                Internship.city.ilike(pattern),
                Internship.state.ilike(pattern),
                Internship.description.ilike(pattern),
                Internship.eligible_degrees.ilike(pattern)
            )
        )

    # 2. Work Mode
    if mode and mode.lower() != "all":
        query = query.filter(Internship.work_mode.ilike(f"%{mode}%"))

    # 3. Category / Domain
    if category and category.lower() != "all":
        query = query.filter(
            or_(
                Internship.category.ilike(f"%{category}%"),
                Internship.industry.ilike(f"%{category}%")
            )
        )

    # 4. Organisation Type
    if org_type and org_type.lower() != "all":
        if org_type.lower() == "government":
            query = query.filter(
                or_(
                    Internship.organisation_type.ilike("%Government%"),
                    Internship.organisation_type.ilike("%Defence%"),
                    Internship.organisation_type.ilike("%Ministry%")
                )
            )
        elif org_type.lower() == "research":
            query = query.filter(
                or_(
                    Internship.organisation_type.ilike("%Research%"),
                    Internship.organisation_type.ilike("%University%")
                )
            )
        else:
            query = query.filter(Internship.organisation_type.ilike(f"%{org_type}%"))

    # 5. State & City
    if state and state.lower() != "all":
        query = query.filter(
            or_(
                Internship.state.ilike(f"%{state}%"),
                Internship.is_pan_india == True,
                Internship.work_mode == "Remote"
            )
        )

    if city and city.lower() != "all":
        query = query.filter(Internship.city.ilike(f"%{city}%"))

    # 6. Stipend Tiers
    if stipend_tier:
        if stipend_tier == "unpaid":
            query = query.filter(Internship.is_unpaid == True)
        elif stipend_tier == "1-5k":
            query = query.filter(and_(Internship.stipend_min >= 1000, Internship.stipend_min <= 5000))
        elif stipend_tier == "5-10k":
            query = query.filter(and_(Internship.stipend_min >= 5000, Internship.stipend_min <= 10000))
        elif stipend_tier == "10-20k":
            query = query.filter(and_(Internship.stipend_min >= 10000, Internship.stipend_min <= 20000))
        elif stipend_tier == "20-30k":
            query = query.filter(and_(Internship.stipend_min >= 20000, Internship.stipend_min <= 30000))
        elif stipend_tier == "30k+":
            query = query.filter(Internship.stipend_min >= 30000)

    # 7. Duration
    if duration_tier:
        if duration_tier == "1m":
            query = query.filter(Internship.duration_value <= 1)
        elif duration_tier == "2-3m":
            query = query.filter(and_(Internship.duration_value >= 2, Internship.duration_value <= 3))
        elif duration_tier == "4-6m":
            query = query.filter(and_(Internship.duration_value >= 4, Internship.duration_value <= 6))
        elif duration_tier == "6m+":
            query = query.filter(Internship.duration_value > 6)

    # 8. PPO / Credits / Verification
    if ppo == "1" or ppo.lower() == "true":
        query = query.filter(Internship.ppo_available == True)

    if credits == "1" or credits.lower() == "true":
        query = query.filter(Internship.academic_credit_available == True)

    if verified_only == "1" or verified_only.lower() == "true":
        query = query.filter(Internship.verification_status.in_(["VERIFIED", "SOURCE_VERIFIED"]))

    # 9. Explainable Sorting
    if sort_by == "deadline":
        query = query.order_by(Internship.application_deadline.asc().nullslast())
    elif sort_by == "newest":
        query = query.order_by(Internship.id.desc())
    elif sort_by == "stipend_high":
        query = query.order_by(Internship.stipend_min.desc())
    elif sort_by == "stipend_low":
        query = query.order_by(Internship.stipend_min.asc())
    elif sort_by == "duration_short":
        query = query.order_by(Internship.duration_value.asc())
    elif sort_by == "duration_long":
        query = query.order_by(Internship.duration_value.desc())
    elif sort_by == "verified":
        query = query.order_by(Internship.verification_status.asc(), Internship.id.desc())
    else:
        # Default relevant sort: prioritize statutory schemes, then deadline
        query = query.order_by(Internship.scheme_name.isnot(None).desc(), Internship.id.desc())

    return query


# =========================================================================
# 1. NATIONAL INTERNSHIP EXPLORER (PAGE & SSR)
# =========================================================================
@internship.route("/")
def internship_list():
    page = request.args.get("page", 1, type=int)
    per_page = 12

    query = build_internship_query(request.args)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    internships = pagination.items

    # Pre-calculate taxonomies for filters
    categories_raw = db.session.query(Internship.category).filter(Internship.category.isnot(None)).distinct().all()
    categories = sorted(list(set(c[0] for c in categories_raw if c[0])))

    states_raw = db.session.query(Internship.state).filter(Internship.state.isnot(None)).distinct().all()
    states = sorted(list(set(s[0] for s in states_raw if s[0] and s[0] != "All India")))

    org_types_raw = db.session.query(Internship.organisation_type).filter(Internship.organisation_type.isnot(None)).distinct().all()
    org_types = sorted(list(set(ot[0] for ot in org_types_raw if ot[0])))

    # User saved IDs
    saved_internship_ids = set()
    user_profile_data = None
    if session.get("user_id"):
        user_saved = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="internship"
        ).all()
        saved_internship_ids = {s.item_id for s in user_saved}

        # Try to load student profile for match preview
        profile = StudentProfile.query.filter_by(user_id=session["user_id"]).first()
        if profile:
            user_profile_data = {
                "degree": profile.degree or profile.education_level or "B.Tech",
                "skills": profile.skills or "",
                "target_career": profile.target_career or "",
                "work_mode": profile.preferred_mode or "Any",
                "city": profile.city or "",
                "state": profile.state or "",
                "percentage": profile.percentage or 75.0
            }

    # Match scores for items if profile exists
    match_scores = {}
    if user_profile_data:
        for it in internships:
            m = InternshipMatchingEngine.compute_match(user_profile_data, it)
            match_scores[it.id] = m

    # Total national statistics
    total_national_count = Internship.query.filter_by(is_active=True).count()
    govt_count = Internship.query.filter(
        Internship.is_active == True,
        or_(
            Internship.organisation_type.ilike("%Government%"),
            Internship.organisation_type.ilike("%Defence%"),
            Internship.scheme_name.isnot(None)
        )
    ).count()
    remote_count = Internship.query.filter_by(is_active=True, work_mode="Remote").count()

    return render_template(
        "internship/list.html",
        internships=internships,
        pagination=pagination,
        categories=categories,
        states=states,
        org_types=org_types,
        saved_internship_ids=saved_internship_ids,
        match_scores=match_scores,
        total_national_count=total_national_count,
        govt_count=govt_count,
        remote_count=remote_count,
        filters=request.args
    )


# =========================================================================
# 2. LIVE ASYNC SEARCH API (JSON FOR DYNAMIC LIVE FILTERING)
# =========================================================================
@internship.route("/api/search")
def api_search():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 12, type=int)

    query = build_internship_query(request.args)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    saved_internship_ids = set()
    if session.get("user_id"):
        user_saved = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="internship"
        ).all()
        saved_internship_ids = {s.item_id for s in user_saved}

    items_data = []
    for it in pagination.items:
        status_label, status_badge_class, _ = it.display_status
        items_data.append({
            "id": it.id,
            "title": it.title,
            "slug": it.slug,
            "organisation_name": it.organisation_name,
            "organisation_type": it.organisation_type,
            "scheme_name": it.scheme_name,
            "category": it.category,
            "work_mode": it.work_mode,
            "location": it.location or f"{it.city or ''}, {it.state or ''}",
            "city": it.city,
            "state": it.state,
            "duration": it.duration_text or f"{it.duration_value} {it.duration_unit}",
            "stipend": it.stipend or ("₹" + str(it.stipend_min) if it.stipend_min else "Provided"),
            "skills": it.skills_list[:4],
            "deadline_text": it.deadline_text,
            "status_label": status_label,
            "status_class": status_badge_class,
            "verification_status": it.verification_status,
            "ppo_available": it.ppo_available,
            "academic_credit_available": it.academic_credit_available,
            "apply_url": url_for("internship.apply_redirect", id=it.id),
            "detail_url": url_for("internship.internship_detail", slug=it.slug),
            "is_saved": it.id in saved_internship_ids
        })

    return jsonify({
        "success": True,
        "total_results": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "has_prev": pagination.has_prev,
        "has_next": pagination.has_next,
        "internships": items_data
    })


# =========================================================================
# 3. SPECIALIZED NATIONAL HUBS
# =========================================================================
@internship.route("/government")
def government_hub():
    """Hub for statutory central & state government initiatives (TULIP, NHAI, Army, etc.)."""
    req_args = request.args.to_dict()
    req_args["org_type"] = "Government"
    return redirect(url_for("internship.internship_list", **req_args))


@internship.route("/corporate")
def corporate_hub():
    """Hub for corporate, MNC, and tech industry internship drives."""
    req_args = request.args.to_dict()
    req_args["org_type"] = "Corporate"
    return redirect(url_for("internship.internship_list", **req_args))


@internship.route("/research")
def research_hub():
    """Hub for research institutions (DRDO, ISRO, C-DAC, CSIR, ICMR, Universities)."""
    req_args = request.args.to_dict()
    req_args["org_type"] = "Research"
    return redirect(url_for("internship.internship_list", **req_args))


@internship.route("/remote")
def remote_hub():
    """Hub for remote / work-from-home verified opportunities."""
    req_args = request.args.to_dict()
    req_args["mode"] = "Remote"
    return redirect(url_for("internship.internship_list", **req_args))


@internship.route("/state/<state_name>")
def state_hub(state_name):
    """Hub for internships localized to a specific Indian state or territory."""
    req_args = request.args.to_dict()
    req_args["state"] = state_name
    return redirect(url_for("internship.internship_list", **req_args))


# =========================================================================
# 4. INTERNSHIP DETAIL DOSSIER
# =========================================================================
@internship.route("/<slug>")
def internship_detail(slug):
    # Lookup by slug, fallback to ID if numeric
    item = Internship.query.filter_by(slug=slug).first()
    if not item and slug.isdigit():
        item = Internship.query.get(int(slug))
    if not item:
        # Check by ID if slug format like title-name-123
        parts = slug.split("-")
        if parts[-1].isdigit():
            item = Internship.query.get(int(parts[-1]))

    if not item:
        flash("The requested internship opportunity could not be found or has expired.", "warning")
        return redirect(url_for("internship.internship_list"))

    # Student matching evaluation
    match_result = None
    is_saved = False
    if session.get("user_id"):
        saved_rec = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="internship",
            item_id=item.id
        ).first()
        is_saved = bool(saved_rec)

        profile = StudentProfile.query.filter_by(user_id=session["user_id"]).first()
        if profile:
            profile_data = {
                "degree": profile.degree or profile.education_level or "B.Tech",
                "skills": profile.skills or "",
                "target_career": profile.target_career or "",
                "work_mode": profile.preferred_mode or "Any",
                "city": profile.city or "",
                "state": profile.state or "",
                "percentage": profile.percentage or 75.0
            }
            match_result = InternshipMatchingEngine.compute_match(profile_data, item)

    # Related Careers
    category_pattern = f"%{item.category or 'Technology'}%"
    related_careers = Career.query.filter(
        or_(
            Career.title.ilike(category_pattern),
            Career.category.ilike(category_pattern),
            Career.industry.ilike(category_pattern)
        )
    ).limit(4).all()

    # Related Courses
    related_courses = Course.query.limit(4).all()

    # Similar Internships
    similar_internships = Internship.query.filter(
        Internship.id != item.id,
        Internship.is_active == True,
        or_(
            Internship.category == item.category,
            Internship.organisation_id == item.organisation_id
        )
    ).limit(3).all()

    return render_template(
        "internship/detail.html",
        internship=item,
        match_result=match_result,
        is_saved=is_saved,
        related_careers=related_careers,
        related_courses=related_courses,
        similar_internships=similar_internships
    )


# =========================================================================
# 5. ORGANISATION DOSSIER
# =========================================================================
@internship.route("/organisation/<slug>")
def organisation_detail(slug):
    org = Organisation.query.filter_by(slug=slug).first_or_404()
    active_internships = Internship.query.filter_by(
        organisation_id=org.id,
        is_active=True
    ).all()

    return render_template(
        "internship/organisation.html",
        organisation=org,
        internships=active_internships
    )


# =========================================================================
# 6. BOOKMARK / SAVE TOGGLE
# =========================================================================
@internship.route("/save/<int:internship_id>")
def toggle_save(internship_id):
    if "user_id" not in session:
        flash("Please log in to save internships to your profile.", "info")
        return redirect(url_for("auth.login"))

    item = Internship.query.get_or_404(internship_id)

    # Sync with SavedOpportunity
    saved_opp = SavedOpportunity.query.filter_by(
        user_id=session["user_id"],
        opportunity_type="internship",
        item_id=internship_id
    ).first()

    # Sync with SavedInternship
    saved_direct = SavedInternship.query.filter_by(
        user_id=session["user_id"],
        internship_id=internship_id
    ).first()

    if saved_opp or saved_direct:
        if saved_opp:
            db.session.delete(saved_opp)
        if saved_direct:
            db.session.delete(saved_direct)
        db.session.commit()
        flash(f"{item.title} removed from saved internships.", "info")
    else:
        new_opp = SavedOpportunity(
            user_id=session["user_id"],
            opportunity_type="internship",
            item_id=internship_id,
            title=item.title
        )
        new_direct = SavedInternship(
            user_id=session["user_id"],
            internship_id=internship_id
        )
        db.session.add(new_opp)
        db.session.add(new_direct)
        db.session.commit()
        flash(f"{item.title} saved to your profile!", "success")

    return redirect(request.referrer or url_for("internship.internship_list"))


# =========================================================================
# 7. STUDENT APPLICATION TRACKER
# =========================================================================
@internship.route("/tracker")
def student_tracker():
    if "user_id" not in session:
        flash("Please log in to access your personal internship application tracker.", "info")
        return redirect(url_for("auth.login"))

    trackers = StudentInternshipTracker.query.filter_by(user_id=session["user_id"]).order_by(StudentInternshipTracker.updated_at.desc()).all()
    saved_items = SavedInternship.query.filter_by(user_id=session["user_id"]).all()

    return render_template(
        "internship/tracker.html",
        trackers=trackers,
        saved_items=saved_items
    )


@internship.route("/tracker/add/<int:internship_id>", methods=["POST"])
def add_to_tracker(internship_id):
    if "user_id" not in session:
        flash("Please log in to track internships.", "info")
        return redirect(url_for("auth.login"))

    item = Internship.query.get_or_404(internship_id)
    existing = StudentInternshipTracker.query.filter_by(
        user_id=session["user_id"],
        internship_id=internship_id
    ).first()

    status = request.form.get("status", "Planning to Apply")
    notes = request.form.get("notes", "")

    if not existing:
        tracker = StudentInternshipTracker(
            user_id=session["user_id"],
            internship_id=internship_id,
            status=status,
            notes=notes
        )
        db.session.add(tracker)
        db.session.commit()
        flash(f"Added {item.title} to your application tracker as '{status}'.", "success")
    else:
        existing.status = status
        if notes:
            existing.notes = notes
        db.session.commit()
        flash(f"Updated tracking status for {item.title} to '{status}'.", "success")

    return redirect(request.referrer or url_for("internship.student_tracker"))


@internship.route("/tracker/update/<int:tracker_id>", methods=["POST"])
def update_tracker(tracker_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    tracker = StudentInternshipTracker.query.filter_by(
        id=tracker_id,
        user_id=session["user_id"]
    ).first_or_404()

    tracker.status = request.form.get("status", tracker.status)
    tracker.application_number = request.form.get("application_number", tracker.application_number)
    tracker.notes = request.form.get("notes", tracker.notes)
    db.session.commit()

    flash("Application tracking updated.", "success")
    return redirect(url_for("internship.student_tracker"))


# =========================================================================
# 8. VERIFIED OUTBOUND APPLY REDIRECTOR
# =========================================================================
@internship.route("/apply/<int:id>")
def apply_redirect(id):
    """
    Safely resolves and redirects student to the authentic official application portal.
    Logs application tracking if student is authenticated.
    """
    item = Internship.query.get_or_404(id)
    target_url = item.primary_apply_url

    if not target_url or not str(target_url).startswith("http"):
        org = (item.organisation_name or "").lower()
        if "infosys" in org:
            target_url = "https://career.infosys.com/"
        elif "tcs" in org:
            target_url = "https://www.tcs.com/careers"
        elif "drdo" in org or "cair" in org:
            target_url = "https://rac.gov.in/"
        elif "bel" in org:
            target_url = "https://bel-india.in/"
        elif "sci" in org or "supreme court" in org:
            target_url = "https://www.sci.gov.in/recruitment/"
        elif "icmr" in org:
            target_url = "https://icmr.gov.in/"
        else:
            target_url = "https://internship.aicte-india.org/internships"

    # Auto-track for logged in students
    if session.get("user_id"):
        try:
            tracker = StudentInternshipTracker.query.filter_by(
                user_id=session["user_id"],
                internship_id=item.id
            ).first()
            if not tracker:
                tracker = StudentInternshipTracker(
                    user_id=session["user_id"],
                    internship_id=item.id,
                    status="Applied",
                    notes=f"Directed to verified portal: {target_url}"
                )
                db.session.add(tracker)
                db.session.commit()
        except Exception:
            pass

    return redirect(target_url)