from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    jsonify
)
from sqlalchemy import or_, func

from extensions import db
from models.exam import GovernmentExam
from models.saved_opportunity import SavedOpportunity
from models.student_profile import StudentProfile
from models.career import Career

exam = Blueprint(
    "exam",
    __name__,
    url_prefix="/exams"
)


# =========================================================================
# 1. EXAM DISCOVERY PORTAL (Main Explorer with Combinable Filters & Search)
# =========================================================================

@exam.route("/")
def exam_list():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    exam_type = request.args.get("type", "").strip()
    qualification = request.args.get("qualification", "").strip()
    stream = request.args.get("stream", "").strip()
    state = request.args.get("state", "").strip()
    status = request.args.get("status", "").strip()
    sort_by = request.args.get("sort", "name_asc").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 12

    # Base query
    query = GovernmentExam.query

    # 1. Global Search across multiple attributes
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                GovernmentExam.exam_name.ilike(pattern),
                GovernmentExam.short_name.ilike(pattern),
                GovernmentExam.conducted_by.ilike(pattern),
                GovernmentExam.category.ilike(pattern),
                GovernmentExam.sub_category.ilike(pattern),
                GovernmentExam.qualification.ilike(pattern),
                GovernmentExam.streams.ilike(pattern),
                GovernmentExam.description.ilike(pattern),
                GovernmentExam.career_opportunities.ilike(pattern)
            )
        )

    # 2. Combinable Filters
    if category:
        query = query.filter(GovernmentExam.category == category)

    if exam_type:
        query = query.filter(GovernmentExam.exam_type.ilike(f"%{exam_type}%"))

    if qualification:
        query = query.filter(
            or_(
                GovernmentExam.qualification.ilike(f"%{qualification}%"),
                GovernmentExam.minimum_qualification.ilike(f"%{qualification}%")
            )
        )

    if stream:
        query = query.filter(
            or_(
                GovernmentExam.streams.ilike(f"%{stream}%"),
                GovernmentExam.streams.ilike("%any%")
            )
        )

    if state and state != "All":
        if state == "All India":
            query = query.filter(GovernmentExam.national_or_state == "National")
        else:
            query = query.filter(GovernmentExam.state.ilike(f"%{state}%"))

    if status:
        query = query.filter(GovernmentExam.status == status)

    # 3. Dynamic Ordering
    if sort_by == "name_desc":
        query = query.order_by(GovernmentExam.exam_name.desc())
    elif sort_by == "newest":
        query = query.order_by(GovernmentExam.id.desc())
    elif sort_by == "status":
        query = query.order_by(GovernmentExam.status.asc())
    else:
        query = query.order_by(GovernmentExam.exam_name.asc())

    # 4. Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    exams = pagination.items

    # 5. Dynamic Counts from Database
    total_exams_count = GovernmentExam.query.count()
    govt_recruitment_count = GovernmentExam.query.filter(
        or_(
            GovernmentExam.exam_type.ilike("%recruitment%"),
            GovernmentExam.category.ilike("%civil%"),
            GovernmentExam.category.ilike("%railway%"),
            GovernmentExam.category.ilike("%bank%"),
            GovernmentExam.category.ilike("%police%")
        )
    ).count()
    entrance_exams_count = GovernmentExam.query.filter(
        GovernmentExam.exam_type.ilike("%entrance%")
    ).count()
    state_exams_count = GovernmentExam.query.filter(
        GovernmentExam.national_or_state == "State"
    ).count()
    professional_exams_count = GovernmentExam.query.filter(
        or_(
            GovernmentExam.exam_type.ilike("%professional%"),
            GovernmentExam.category.ilike("%professional%"),
            GovernmentExam.category.ilike("%commerce%")
        )
    ).count()

    # 6. Filter Options
    categories_raw = db.session.query(GovernmentExam.category).distinct().all()
    categories = sorted([c[0] for c in categories_raw if c[0]])

    types_raw = db.session.query(GovernmentExam.exam_type).distinct().all()
    exam_types = sorted([t[0] for t in types_raw if t[0]])

    states_raw = db.session.query(GovernmentExam.state).distinct().all()
    states = sorted([s[0] for s in states_raw if s[0] and s[0] != "All India"])

    # 7. Saved IDs for active user
    saved_exam_ids = set()
    if session.get("user_id"):
        user_saved = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="exam"
        ).all()
        saved_exam_ids = {s.item_id for s in user_saved}

    return render_template(
        "exam/list.html",
        exams=exams,
        pagination=pagination,
        search=search,
        selected_category=category,
        selected_type=exam_type,
        selected_qualification=qualification,
        selected_stream=stream,
        selected_state=state,
        selected_status=status,
        selected_sort=sort_by,
        categories=categories,
        exam_types=exam_types,
        states=states,
        saved_exam_ids=saved_exam_ids,
        counts={
            "total": total_exams_count,
            "government": govt_recruitment_count,
            "entrance": entrance_exams_count,
            "state": state_exams_count,
            "professional": professional_exams_count
        }
    )


# =========================================================================
# 2. DEDICATED EXAM DETAIL DOSSIER
# =========================================================================

@exam.route("/<int:exam_id>")
@exam.route("/slug/<string:slug>")
def exam_detail(exam_id=None, slug=None):
    if exam_id:
        exam_obj = GovernmentExam.query.get_or_404(exam_id)
    elif slug:
        exam_obj = GovernmentExam.query.filter_by(slug=slug).first_or_404()
    else:
        abort(404)

    # Check if saved by current student
    is_saved = False
    if session.get("user_id"):
        is_saved = SavedOpportunity.query.filter_by(
            user_id=session["user_id"],
            opportunity_type="exam",
            item_id=exam_id
        ).first() is not None

    # Find closely related careers
    related_careers_list = []
    if exam_obj.career_opportunities or exam_obj.category:
        tokens = [exam_obj.category] if exam_obj.category else []
        if exam_obj.short_name:
            tokens.append(exam_obj.short_name)
        if exam_obj.sub_category:
            tokens.append(exam_obj.sub_category)

        clauses = [Career.category.ilike(f"%{t}%") for t in tokens if t]
        if clauses:
            related_careers_list = Career.query.filter(or_(*clauses)).limit(4).all()

    # Find similar / alternate exams in same category
    similar_exams = GovernmentExam.query.filter(
        GovernmentExam.category == exam_obj.category,
        GovernmentExam.id != exam_obj.id
    ).limit(3).all()

    return render_template(
        "exam/details.html",
        exam=exam_obj,
        is_saved=is_saved,
        related_careers=related_careers_list,
        similar_exams=similar_exams
    )


# =========================================================================
# 3. DEDICATED EXAM CALENDAR & DEADLINES
# =========================================================================

@exam.route("/calendar")
def exam_calendar():
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()

    query = GovernmentExam.query.filter(
        or_(
            GovernmentExam.exam_date.isnot(None),
            GovernmentExam.application_end_date.isnot(None),
            GovernmentExam.status.in_(["UPCOMING", "APPLICATION_OPEN", "NOTIFICATION_EXPECTED"])
        )
    )

    if category:
        query = query.filter(GovernmentExam.category == category)

    if status:
        query = query.filter(GovernmentExam.status == status)

    scheduled_exams = query.order_by(GovernmentExam.exam_name.asc()).all()

    categories_raw = db.session.query(GovernmentExam.category).distinct().all()
    categories = sorted([c[0] for c in categories_raw if c[0]])

    return render_template(
        "exam/calendar.html",
        exams=scheduled_exams,
        categories=categories,
        selected_category=category,
        selected_status=status
    )


# =========================================================================
# 4. "WHO CAN APPLY?" INTERACTIVE ELIGIBILITY FINDER
# =========================================================================

@exam.route("/eligibility", methods=["GET", "POST"])
def who_can_apply():
    qualification = request.args.get("qualification", "").strip()
    stream = request.args.get("stream", "").strip()
    category_pref = request.args.get("category", "").strip()

    matched_exams = []
    has_searched = bool(qualification or stream or category_pref)

    if has_searched:
        query = GovernmentExam.query

        if qualification:
            query = query.filter(
                or_(
                    GovernmentExam.qualification.ilike(f"%{qualification}%"),
                    GovernmentExam.minimum_qualification.ilike(f"%{qualification}%")
                )
            )

        if stream and stream != "Any":
            query = query.filter(
                or_(
                    GovernmentExam.streams.ilike(f"%{stream}%"),
                    GovernmentExam.streams.ilike("%any%"),
                    GovernmentExam.streams.is_(None)
                )
            )

        if category_pref:
            query = query.filter(GovernmentExam.category.ilike(f"%{category_pref}%"))

        matched_exams = query.order_by(GovernmentExam.exam_name.asc()).limit(50).all()

    return render_template(
        "exam/eligibility_finder.html",
        matched_exams=matched_exams,
        has_searched=has_searched,
        selected_qualification=qualification,
        selected_stream=stream,
        selected_category=category_pref
    )


# =========================================================================
# 5. AI EXAM DISCOVERY API ("Find Exams For Me" - Strictly from DB)
# =========================================================================

@exam.route("/ai-discovery", methods=["POST"])
def ai_exam_discovery():
    data = request.get_json(silent=True) or {}
    user_query = data.get("query", "").strip().lower()

    if not user_query:
        return jsonify({
            "success": False,
            "message": "Please enter your education background or stream to find examinations."
        })

    # Strict multi-factor matching based on query tokens against database records only
    tokens = [t.strip() for t in user_query.replace(",", " ").split() if len(t.strip()) > 2]
    
    clauses = []
    for token in tokens[:6]:
        pattern = f"%{token}%"
        clauses.append(GovernmentExam.exam_name.ilike(pattern))
        clauses.append(GovernmentExam.category.ilike(pattern))
        clauses.append(GovernmentExam.streams.ilike(pattern))
        clauses.append(GovernmentExam.qualification.ilike(pattern))
        clauses.append(GovernmentExam.career_opportunities.ilike(pattern))

    results = []
    if clauses:
        matching_exams = GovernmentExam.query.filter(or_(*clauses)).limit(6).all()
        for ex in matching_exams:
            reasons = []
            if ex.qualification and any(t in ex.qualification.lower() for t in tokens):
                reasons.append(f"Matches your educational eligibility: {ex.qualification}")
            if ex.streams and any(t in ex.streams.lower() for t in tokens):
                reasons.append(f"Aligned with your academic stream: {ex.streams}")
            if ex.category and any(t in ex.category.lower() for t in tokens):
                reasons.append(f"Matches your category interest in {ex.category}")
            if not reasons:
                reasons.append(f"Recognized opportunity under {ex.conducting_body}")

            results.append({
                "id": ex.id,
                "name": ex.exam_name,
                "short_name": ex.short_name,
                "conducted_by": ex.conducted_by,
                "category": ex.category,
                "qualification": ex.qualification,
                "status": ex.display_status[0],
                "status_badge": ex.display_status[1],
                "official_website": ex.official_website or ex.official_url,
                "detail_url": url_for("exam.exam_detail", exam_id=ex.id),
                "reasons": reasons
            })

    return jsonify({
        "success": True,
        "results": results,
        "count": len(results)
    })


# =========================================================================
# 6. BOOKMARK / SAVE EXAM TOGGLE
# =========================================================================

@exam.route("/save/<int:exam_id>")
def toggle_save(exam_id):
    if "user_id" not in session:
        flash("Please log in to save examinations to your profile.", "info")
        return redirect(url_for("auth.login"))

    exam_obj = GovernmentExam.query.get_or_404(exam_id)

    existing = SavedOpportunity.query.filter_by(
        user_id=session["user_id"],
        opportunity_type="exam",
        item_id=exam_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f"{exam_obj.exam_name} removed from your saved list.", "info")
    else:
        saved = SavedOpportunity(
            user_id=session["user_id"],
            opportunity_type="exam",
            item_id=exam_id,
            title=exam_obj.exam_name
        )
        db.session.add(saved)
        db.session.commit()
        flash(f"{exam_obj.exam_name} saved to your profile!", "success")

    return redirect(request.referrer or url_for("exam.exam_list"))