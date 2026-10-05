from flask import Blueprint, render_template, request, abort, session, redirect, url_for, flash, jsonify
from sqlalchemy import or_, and_, func

from extensions import db
from models.college import College
from models.course import Course, CollegeCourse
from models.career import Career
from models.saved_college import SavedCollege

college = Blueprint(
    "college",
    __name__,
    url_prefix="/colleges"
)


# =========================================================================
# 1. COLLEGE DIRECTORY (Multi-Factor Search, Combinable Filters & Pagination)
# =========================================================================

@college.route("/search")
@college.route("/filter")
@college.route("/")
def college_list():
    search = request.args.get("search", "").strip()
    state = request.args.get("state", "").strip()
    city = request.args.get("city", "").strip()
    inst_type = request.args.get("type", "").strip()
    gov_priv = request.args.get("gov_priv", "").strip()
    course_id = request.args.get("course_id", type=int) or request.args.get("course", type=int)
    discipline = request.args.get("discipline", "").strip()
    stream = request.args.get("stream", "").strip()
    sort_by = request.args.get("sort", "name_asc").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 24

    query = College.query

    # 1. Full-Text Search across Database Fields
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                College.aishe_code.ilike(pattern),
                College.name.ilike(pattern),
                College.short_name.ilike(pattern),
                College.university_name.ilike(pattern),
                College.city.ilike(pattern),
                College.district.ilike(pattern),
                College.state.ilike(pattern),
                College.institution_type.ilike(pattern),
                College.course.ilike(pattern)
            )
        )

    # 2. Combinable Location Filters
    if state and state != "All":
        query = query.filter(College.state == state)

    if city and city != "All":
        query = query.filter(College.city.ilike(f"%{city}%"))

    # 3. Governance Filter (Government vs Private)
    if gov_priv and gov_priv != "All":
        query = query.filter(College.government_private.ilike(f"%{gov_priv}%"))

    # 4. Institution Type Filter
    if inst_type and inst_type != "All":
        query = query.filter(
            or_(
                College.institution_type.ilike(f"%{inst_type}%"),
                College.college_type.ilike(f"%{inst_type}%")
            )
        )

    # 5. Course-Specific Relational Filter (Exact relational match via CollegeCourse)
    if course_id:
        subquery = db.session.query(CollegeCourse.college_id).filter(CollegeCourse.course_id == course_id)
        query = query.filter(College.id.in_(subquery))

    # 6. Discipline / Stream Filter
    if discipline and discipline != "All":
        course_subquery = db.session.query(CollegeCourse.college_id).join(Course).filter(
            Course.discipline.ilike(f"%{discipline}%")
        )
        query = query.filter(
            or_(
                College.id.in_(course_subquery),
                College.course.ilike(f"%{discipline}%")
            )
        )

    if stream and stream != "All":
        stream_subquery = db.session.query(CollegeCourse.college_id).join(Course).filter(
            or_(
                Course.stream.ilike(f"%{stream}%"),
                Course.stream.ilike("%Any%")
            )
        )
        query = query.filter(
            or_(
                College.id.in_(stream_subquery),
                College.course.ilike(f"%{stream}%")
            )
        )

    # 7. Sorting
    if sort_by == "name_desc":
        query = query.order_by(College.name.desc())
    elif sort_by == "nirf":
        # Sort by NIRF rank ascending (nulls last)
        query = query.order_by(
            func.coalesce(College.nirf_rank, 99999).asc(),
            College.name.asc()
        )
    elif sort_by == "state":
        query = query.order_by(College.state.asc(), College.name.asc())
    elif sort_by == "newest":
        query = query.order_by(College.id.desc())
    else:
        query = query.order_by(College.name.asc())

    # 8. Pagination (Database-Level LIMIT/OFFSET)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    colleges = pagination.items

    # 9. Dynamic Metrics (Computed strictly from DB)
    total_institutions = College.query.count()
    total_universities = College.query.filter(
        or_(
            College.institution_category == "University",
            College.institution_type.ilike("%university%")
        )
    ).count()
    total_colleges = College.query.filter(
        or_(
            College.institution_category == "College",
            College.institution_type.ilike("%college%")
        )
    ).count()
    total_government = College.query.filter(
        College.government_private.ilike("%government%")
    ).count()
    total_private = College.query.filter(
        College.government_private.ilike("%private%")
    ).count()
    total_courses_count = Course.query.count()

    # 10. Distinct Filter Options
    states_raw = db.session.query(College.state).distinct().all()
    states = sorted([s[0] for s in states_raw if s[0]])

    types_raw = db.session.query(College.institution_type).distinct().all()
    institution_types = sorted([t[0] for t in types_raw if t[0]])

    disciplines_raw = db.session.query(Course.discipline).distinct().all()
    disciplines = sorted([d[0] for d in disciplines_raw if d[0]])

    all_courses = Course.query.order_by(Course.name.asc()).all()

    # 11. Saved College IDs for active user
    saved_college_ids = set()
    if session.get("user_id"):
        user_saved = SavedCollege.query.filter_by(user_id=session["user_id"]).all()
        saved_college_ids = {s.college_id for s in user_saved}

    # Selected course name for UI label
    selected_course_obj = None
    if course_id:
        selected_course_obj = Course.query.get(course_id)

    return render_template(
        "college/list.html",
        colleges=colleges,
        pagination=pagination,
        search=search,
        selected_state=state,
        selected_city=city,
        selected_type=inst_type,
        selected_gov_priv=gov_priv,
        selected_course_id=course_id,
        selected_course=selected_course_obj,
        selected_discipline=discipline,
        selected_stream=stream,
        selected_sort=sort_by,
        states=states,
        institution_types=institution_types,
        disciplines=disciplines,
        all_courses=all_courses,
        saved_college_ids=saved_college_ids,
        counts={
            "total": total_institutions,
            "universities": total_universities,
            "colleges": total_colleges,
            "government": total_government,
            "private": total_private,
            "courses": total_courses_count
        }
    )


# =========================================================================
# 2. COLLEGE DETAIL DOSSIER
# =========================================================================

@college.route("/<int:college_id>")
@college.route("/<int:college_id>/courses")
@college.route("/<int:college_id>/university")
def college_detail(college_id):
    col = College.query.get_or_404(college_id)

    is_saved = False
    if session.get("user_id"):
        is_saved = SavedCollege.query.filter_by(
            user_id=session["user_id"],
            college_id=col.id
        ).first() is not None

    # Retrieve mapped courses
    college_courses = CollegeCourse.query.filter_by(college_id=col.id).join(Course).all()

    # Same-state related institutions
    related = College.query.filter(
        College.state == col.state,
        College.id != col.id
    ).order_by(func.random()).limit(3).all()

    # Link to related careers based on mapped disciplines
    career_disciplines = set()
    for cc in college_courses:
        if cc.course and cc.course.discipline:
            career_disciplines.add(cc.course.discipline.lower())

    related_careers = []
    if career_disciplines:
        clauses = [Career.category.ilike(f"%{d}%") for d in list(career_disciplines)[:3]]
        related_careers = Career.query.filter(or_(*clauses)).limit(4).all()

    return render_template(
        "college/details.html",
        college=col,
        is_saved=is_saved,
        college_courses=college_courses,
        related=related,
        related_careers=related_careers
    )


# =========================================================================
# 3. COURSE-FIRST EXPLORER (Colleges offering a specific course)
# =========================================================================

@college.route("/course/<int:course_id>")
def colleges_by_course(course_id):
    course = Course.query.get_or_404(course_id)
    state = request.args.get("state", "").strip()
    gov_priv = request.args.get("gov_priv", "").strip()
    page = request.args.get("page", 1, type=int)

    query = College.query.join(CollegeCourse).filter(CollegeCourse.course_id == course.id)

    if state:
        query = query.filter(College.state == state)
    if gov_priv:
        query = query.filter(College.government_private.ilike(f"%{gov_priv}%"))

    query = query.order_by(College.name.asc())
    pagination = query.paginate(page=page, per_page=18, error_out=False)

    states_raw = db.session.query(College.state).join(CollegeCourse).filter(
        CollegeCourse.course_id == course.id
    ).distinct().all()
    available_states = sorted([s[0] for s in states_raw if s[0]])

    saved_college_ids = set()
    if session.get("user_id"):
        user_saved = SavedCollege.query.filter_by(user_id=session["user_id"]).all()
        saved_college_ids = {s.college_id for s in user_saved}

    return render_template(
        "college/course_colleges.html",
        course=course,
        colleges=pagination.items,
        pagination=pagination,
        states=available_states,
        selected_state=state,
        selected_gov_priv=gov_priv,
        saved_college_ids=saved_college_ids
    )


# =========================================================================
# 4. COLLEGE COMPARISON (Side-by-side Matrix for 2-4 Institutions)
# =========================================================================

@college.route("/compare")
def compare_colleges():
    ids_param = request.args.get("ids", "").strip()
    id_list = []
    if ids_param:
        for item in ids_param.split(","):
            try:
                id_list.append(int(item.strip()))
            except ValueError:
                pass

    colleges_to_compare = []
    if id_list:
        colleges_to_compare = College.query.filter(College.id.in_(id_list[:4])).all()

    # All colleges for selection dropdowns
    all_colleges = College.query.with_entities(College.id, College.name, College.city, College.state).order_by(College.name.asc()).all()

    return render_template(
        "college/compare.html",
        colleges=colleges_to_compare,
        all_colleges=all_colleges,
        selected_ids=id_list
    )


# =========================================================================
# 5. "FIND COLLEGES FOR ME" (Guided Discovery Wizard & Page)
# =========================================================================

@college.route("/find")
def college_finder():
    states_raw = db.session.query(College.state).distinct().all()
    states = sorted([s[0] for s in states_raw if s[0]])
    disciplines_raw = db.session.query(Course.discipline).distinct().all()
    disciplines = sorted([d[0] for d in disciplines_raw if d[0]])
    courses = Course.query.order_by(Course.name.asc()).all()

    return render_template(
        "college/finder.html",
        states=states,
        disciplines=disciplines,
        courses=courses
    )


# =========================================================================
# 6. AI COLLEGE DISCOVERY API (Strictly from verified DB records)
# =========================================================================

@college.route("/ai-discovery", methods=["POST"])
def ai_college_discovery():
    data = request.get_json(silent=True) or {}
    query_text = data.get("query", "").strip().lower()
    pref_state = data.get("state", "").strip()
    pref_stream = data.get("stream", "").strip()
    pref_gov = data.get("gov_priv", "").strip()
    course_name = data.get("course", "").strip()

    if not query_text and not pref_state and not course_name and not pref_stream:
        return jsonify({
            "success": False,
            "message": "Please enter your course interest, stream, or preferred state to discover colleges."
        })

    # Token-based multi-factor matching
    tokens = [t.strip() for t in query_text.replace(",", " ").split() if len(t.strip()) > 2]
    
    query = College.query

    if pref_state and pref_state != "All":
        query = query.filter(College.state.ilike(f"%{pref_state}%"))

    if pref_gov and pref_gov != "All":
        query = query.filter(College.government_private.ilike(f"%{pref_gov}%"))

    clauses = []
    for token in tokens[:5]:
        pattern = f"%{token}%"
        clauses.append(College.name.ilike(pattern))
        clauses.append(College.course.ilike(pattern))
        clauses.append(College.city.ilike(pattern))
        clauses.append(College.institution_type.ilike(pattern))

    if course_name:
        clauses.append(College.course.ilike(f"%{course_name}%"))

    if clauses:
        query = query.filter(or_(*clauses))

    results = []
    matched_institutions = query.limit(6).all()

    for col in matched_institutions:
        reasons = []
        if pref_state and col.state and pref_state.lower() in col.state.lower():
            reasons.append(f"Located in your preferred state: {col.state}")
        if col.government_private:
            reasons.append(f"{col.government_private} institution with statutory accreditation")
        if col.institution_type:
            reasons.append(f"Classified as {col.institution_type}")
        if col.nirf_rank:
            reasons.append(f"Ranked #{col.nirf_rank} under NIRF ({col.nirf_category or 'National'})")
        if not reasons:
            reasons.append("Matches your academic search parameters and course interest")

        results.append({
            "id": col.id,
            "name": col.name,
            "short_name": col.short_name,
            "type": col.display_type,
            "location": f"{col.city}, {col.state}",
            "official_website": col.display_website,
            "detail_url": url_for("college.college_detail", college_id=col.id),
            "reasons": reasons
        })

    return jsonify({
        "success": True,
        "results": results,
        "count": len(results)
    })


# =========================================================================
# 7. SAVE / BOOKMARK COLLEGE TOGGLE
# =========================================================================

@college.route("/save/<int:college_id>")
def toggle_save(college_id):
    if "user_id" not in session:
        flash("Please log in to save colleges to your profile.", "info")
        return redirect(url_for("auth.login"))

    col = College.query.get_or_404(college_id)

    existing = SavedCollege.query.filter_by(
        user_id=session["user_id"],
        college_id=college_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f"{col.name} removed from saved colleges.", "info")
    else:
        saved = SavedCollege(
            user_id=session["user_id"],
            college_id=college_id
        )
        db.session.add(saved)
        db.session.commit()
        flash(f"{col.name} saved to your profile!", "success")

    return redirect(request.referrer or url_for("college.college_detail", college_id=college_id))