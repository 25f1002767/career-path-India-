from flask import Blueprint, render_template, request, jsonify, abort, url_for
from sqlalchemy import or_, func

from extensions import db
from models.course import Course, CollegeCourse
from models.college import College
from models.career import Career


course = Blueprint(
    "course",
    __name__,
    url_prefix="/courses"
)


# =========================================================================
# 1. COURSE DIRECTORY & CATALOG
# =========================================================================

@course.route("/")
def course_list():
    search = request.args.get("search", "").strip()
    level = request.args.get("level", "").strip()
    discipline = request.args.get("discipline", "").strip()
    stream = request.args.get("stream", "").strip()
    sort_by = request.args.get("sort", "popular").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 18

    query = Course.query

    # Search with Alias and Full-Text Understanding
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Course.name.ilike(pattern),
                Course.short_name.ilike(pattern),
                Course.aliases.ilike(pattern),
                Course.discipline.ilike(pattern),
                Course.specialization.ilike(pattern),
                Course.description.ilike(pattern)
            )
        )

    # Education Level Filter (UG, PG, Diploma, Integrated)
    if level and level != "All":
        query = query.filter(Course.level == level)

    # Discipline Filter
    if discipline and discipline != "All":
        query = query.filter(Course.discipline.ilike(f"%{discipline}%"))

    # Stream Filter
    if stream and stream != "All":
        query = query.filter(
            or_(
                Course.stream.ilike(f"%{stream}%"),
                Course.stream.ilike("%Any%")
            )
        )

    # Sorting
    if sort_by == "name_asc":
        query = query.order_by(Course.name.asc())
    elif sort_by == "name_desc":
        query = query.order_by(Course.name.desc())
    else:
        # Default: Sort by popularity (number of institutions offering this course)
        subq = (
            db.session.query(
                CollegeCourse.course_id,
                func.count(CollegeCourse.id).label("cc_count")
            )
            .filter(CollegeCourse.verification_status == "VERIFIED")
            .group_by(CollegeCourse.course_id)
            .subquery()
        )
        query = (
            query.outerjoin(subq, Course.id == subq.c.course_id)
            .order_by(func.coalesce(subq.c.cc_count, 0).desc(), Course.name.asc())
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    courses = pagination.items

    # Filter Options
    disciplines_raw = db.session.query(Course.discipline).distinct().all()
    disciplines = sorted([d[0] for d in disciplines_raw if d[0]])

    levels_raw = db.session.query(Course.level).distinct().all()
    levels = sorted([l[0] for l in levels_raw if l[0]])

    # Metrics
    total_courses_count = Course.query.count()
    ug_count = Course.query.filter_by(level="UG").count()
    pg_count = Course.query.filter_by(level="PG").count()
    diploma_count = Course.query.filter_by(level="Diploma").count()
    total_offerings_count = CollegeCourse.query.filter_by(verification_status="VERIFIED").count()

    # Pre-fetch offering counts per course for display
    course_counts = dict(
        db.session.query(
            CollegeCourse.course_id,
            func.count(CollegeCourse.id)
        )
        .filter(CollegeCourse.verification_status == "VERIFIED")
        .group_by(CollegeCourse.course_id)
        .all()
    )

    popular_courses = [
        "B.Sc Mathematics",
        "B.Tech Computer Science & Engineering",
        "BCA (Bachelor of Computer Applications)",
        "MBBS",
        "B.Com (General / Honours)",
        "BA Economics",
        "MBA (Master of Business Administration)",
        "B.Ed (Bachelor of Education)",
        "B.Sc Physics",
        "BA LLB (Integrated Law)"
    ]

    return render_template(
        "course/list.html",
        courses=courses,
        pagination=pagination,
        search=search,
        selected_level=level,
        selected_discipline=discipline,
        selected_stream=stream,
        selected_sort=sort_by,
        disciplines=disciplines,
        levels=levels,
        course_counts=course_counts,
        popular_courses=popular_courses,
        metrics={
            "total": total_courses_count,
            "ug": ug_count,
            "pg": pg_count,
            "diploma": diploma_count,
            "offerings": total_offerings_count
        }
    )


# =========================================================================
# 2. COURSE DOSSIER & OFFERING INSTITUTIONS EXPLORER
# =========================================================================

@course.route("/<int:course_id>")
@course.route("/slug/<string:slug>")
def course_detail(course_id=None, slug=None):
    if course_id:
        c = Course.query.get_or_404(course_id)
    elif slug:
        c = Course.query.filter_by(slug=slug).first_or_404()
    else:
        abort(404)

    state = request.args.get("state", "").strip()
    city = request.args.get("city", "").strip()
    gov_priv = request.args.get("gov_priv", "").strip()
    inst_type = request.args.get("type", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 15

    # Query strictly verified college offerings for this canonical course
    query = (
        db.session.query(CollegeCourse, College)
        .join(College, CollegeCourse.college_id == College.id)
        .filter(
            CollegeCourse.course_id == c.id,
            CollegeCourse.verification_status == "VERIFIED"
        )
    )

    # Location Filters
    if state and state != "All":
        query = query.filter(College.state == state)

    if city and city != "All":
        query = query.filter(
            or_(
                College.city.ilike(f"%{city}%"),
                College.district.ilike(f"%{city}%")
            )
        )

    # Governance Filter
    if gov_priv and gov_priv != "All":
        query = query.filter(College.government_private.ilike(f"%{gov_priv}%"))

    # Institution Type Filter
    if inst_type and inst_type != "All":
        query = query.filter(College.institution_type.ilike(f"%{inst_type}%"))

    # Sorting: NIRF first, then Government, then Name
    query = query.order_by(
        func.coalesce(College.nirf_rank, 99999).asc(),
        College.name.asc()
    )

    total_offering_colleges = query.count()
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    results = pagination.items  # List of tuples: (CollegeCourse, College)

    # Distinct states offering this specific course
    states_raw = (
        db.session.query(College.state)
        .join(CollegeCourse, College.id == CollegeCourse.college_id)
        .filter(
            CollegeCourse.course_id == c.id,
            CollegeCourse.verification_status == "VERIFIED"
        )
        .distinct()
        .all()
    )
    available_states = sorted([s[0] for s in states_raw if s[0]])

    # Institution types offering this course
    types_raw = (
        db.session.query(College.institution_type)
        .join(CollegeCourse, College.id == CollegeCourse.college_id)
        .filter(
            CollegeCourse.course_id == c.id,
            CollegeCourse.verification_status == "VERIFIED"
        )
        .distinct()
        .all()
    )
    available_types = sorted([t[0] for t in types_raw if t[0]])

    # Related Careers linking: Career -> Course -> College
    related_careers = []
    if c.discipline:
        career_clauses = [
            Career.category.ilike(f"%{c.discipline}%"),
            Career.education_required.ilike(f"%{c.name[:10]}%"),
            Career.education_required.ilike(f"%{c.short_name or c.name}%")
        ]
        related_careers = Career.query.filter(or_(*career_clauses)).limit(4).all()

    # If few found, fallback to broader discipline match
    if not related_careers and c.discipline:
        related_careers = Career.query.filter(Career.category.ilike(f"%{c.discipline[:5]}%")).limit(3).all()

    return render_template(
        "course/details.html",
        course=c,
        results=results,
        pagination=pagination,
        total_count=total_offering_colleges,
        states=available_states,
        institution_types=available_types,
        selected_state=state,
        selected_city=city,
        selected_gov_priv=gov_priv,
        selected_type=inst_type,
        related_careers=related_careers
    )


# =========================================================================
# 3. JSON API: COURSE AUTOCOMPLETE & ALIAS SEARCH
# =========================================================================

@course.route("/api/search")
def api_course_search():
    q = request.args.get("q", "").strip()
    if not q or len(q) < 2:
        return jsonify([])

    pattern = f"%{q}%"
    matches = (
        Course.query.filter(
            or_(
                Course.name.ilike(pattern),
                Course.short_name.ilike(pattern),
                Course.aliases.ilike(pattern),
                Course.discipline.ilike(pattern)
            )
        )
        .order_by(Course.name.asc())
        .limit(10)
        .all()
    )

    data = []
    for c in matches:
        data.append({
            "id": c.id,
            "name": c.name,
            "short_name": c.short_name,
            "level": c.level,
            "discipline": c.discipline,
            "institutions_count": c.institution_count,
            "url": url_for("course.course_detail", course_id=c.id)
        })

    return jsonify(data)
