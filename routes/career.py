"""
routes/career.py
==============================================================================
National Career Discovery & Counselling Blueprint
==============================================================================
Comprehensive discovery portal supporting:
- 126+ authentic careers across 14 national sectors
- Multi-factor search & filtering (Category, Stream, Education, Work Mode, Opportunity)
- Dedicated Category / Sector landing pages
- Career Dossier with multi-route pathways, stage roadmaps, relational degree & exam graph
- Interactive Career Fit Explorer ("Am I Suitable for This Career?")
- "Help Me Discover Careers" guided questionnaire
- Reverse discovery: Degree -> Career, Skill -> Career, Subject -> Career
- Career Comparison matrix (up to 4 careers)
- AI Career Counsellor grounded strictly in verified database facts
==============================================================================
"""

import json
from flask import (
    Blueprint,
    render_template,
    request,
    abort,
    session,
    redirect,
    url_for,
    flash,
    jsonify
)
from sqlalchemy import or_, func

from extensions import db
from models.career import Career
from models.career_course import CareerCourse
from models.career_exam import CareerExam
from models.career_skill import CareerSkill
from models.roadmap import CareerRoadmap
from models.course import Course, CollegeCourse
from models.college import College
from models.exam import GovernmentExam
from models.saved_career import SavedCareer
from models.student_profile import StudentProfile
from models.resume import Resume
from services.skill_gap import analyze_skill_gap
from services.career_taxonomy import (
    SECTORS_METADATA,
    get_sector_by_slug,
    calculate_career_fit
)
from services.career_counselling_engine import generate_counsellor_response

career = Blueprint(
    "career",
    __name__,
    url_prefix="/careers"
)


# ============================================================================
# 1. Career Explorer & Multi-Factor Filters
# ============================================================================

@career.route("/")
def career_list():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    stream = request.args.get("stream", "").strip()
    education = request.args.get("education", "").strip()
    work_mode = request.args.get("work_mode", "").strip()
    opportunity = request.args.get("opportunity", "").strip()
    sort_by = request.args.get("sort", "title_asc").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 15

    query = Career.query

    # Search query
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Career.title.ilike(pattern),
                Career.short_description.ilike(pattern),
                Career.description.ilike(pattern),
                Career.sub_category.ilike(pattern),
                Career.industry.ilike(pattern),
                Career.technical_skills.ilike(pattern),
                Career.required_subjects.ilike(pattern),
                Career.category.ilike(pattern)
            )
        )

    # Category / Sector filter
    if category:
        query = query.filter(Career.category == category)

    # Stream filter
    if stream:
        query = query.filter(
            or_(
                Career.preferred_streams.ilike(f"%{stream}%"),
                Career.preferred_streams.ilike("%any%"),
                Career.preferred_streams.ilike("%open%")
            )
        )

    # Education level filter
    if education:
        query = query.filter(Career.minimum_qualification.ilike(f"%{education}%"))

    # Work mode filter
    if work_mode:
        query = query.filter(Career.work_modes.ilike(f"%{work_mode}%"))

    # Opportunity type (Government vs Private)
    if opportunity == "government":
        query = query.filter(Career.government_opportunities != "", Career.government_opportunities.isnot(None))
    elif opportunity == "private":
        query = query.filter(Career.private_opportunities != "", Career.private_opportunities.isnot(None))

    # Sorting
    if sort_by == "title_desc":
        query = query.order_by(Career.title.desc())
    elif sort_by == "newest":
        query = query.order_by(Career.id.desc())
    elif sort_by == "category":
        query = query.order_by(Career.category.asc(), Career.title.asc())
    else:
        query = query.order_by(Career.title.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    careers = pagination.items

    # Fetch sector counts for category pills
    category_counts_raw = (
        db.session.query(Career.category, func.count(Career.id))
        .group_by(Career.category)
        .order_by(func.count(Career.id).desc())
        .all()
    )
    category_counts = {c[0]: c[1] for c in category_counts_raw if c[0]}

    # Total counts for statistics banner
    total_careers_count = Career.query.count()
    total_courses_linked = db.session.query(func.count(CareerCourse.id)).scalar() or 0
    total_exams_linked = db.session.query(func.count(CareerExam.id)).scalar() or 0

    saved_career_ids = set()
    if session.get("user_id"):
        user_saved = SavedCareer.query.filter_by(user_id=session["user_id"]).all()
        saved_career_ids = {s.career_id for s in user_saved}

    return render_template(
        "career/list.html",
        careers=careers,
        pagination=pagination,
        categories=list(SECTORS_METADATA.keys()),
        category_counts=category_counts,
        sectors_metadata=SECTORS_METADATA,
        search=search,
        selected_category=category,
        selected_stream=stream,
        selected_education=education,
        selected_work_mode=work_mode,
        selected_opportunity=opportunity,
        sort_by=sort_by,
        saved_career_ids=saved_career_ids,
        total_careers_count=total_careers_count,
        total_courses_linked=total_courses_linked,
        total_exams_linked=total_exams_linked
    )


# ============================================================================
# 2. Sector / Category Dedicated Landing Page
# ============================================================================

@career.route("/category/<category_slug>")
def career_category(category_slug):
    category_name, sector_meta = get_sector_by_slug(category_slug)
    if not category_name:
        abort(404)

    # Fetch all careers in this sector
    careers = Career.query.filter_by(category=category_name).order_by(Career.title.asc()).all()

    # Distinct subcategories
    subcategories = sorted(list({c.sub_category for c in careers if c.sub_category}))

    # Linked degrees for this sector
    career_ids = [c.id for c in careers]
    linked_course_ids = (
        db.session.query(CareerCourse.course_id)
        .filter(CareerCourse.career_id.in_(career_ids))
        .distinct()
        .all()
    )
    course_ids = [r[0] for r in linked_course_ids]
    linked_courses = Course.query.filter(Course.id.in_(course_ids)).limit(8).all() if course_ids else []

    # Linked exams for this sector
    linked_exam_ids = (
        db.session.query(CareerExam.exam_id)
        .filter(CareerExam.career_id.in_(career_ids))
        .distinct()
        .all()
    )
    exam_ids = [r[0] for r in linked_exam_ids]
    linked_exams = GovernmentExam.query.filter(GovernmentExam.id.in_(exam_ids)).limit(8).all() if exam_ids else []

    saved_career_ids = set()
    if session.get("user_id"):
        user_saved = SavedCareer.query.filter_by(user_id=session["user_id"]).all()
        saved_career_ids = {s.career_id for s in user_saved}

    return render_template(
        "career/category.html",
        category_name=category_name,
        sector_meta=sector_meta,
        careers=careers,
        subcategories=subcategories,
        linked_courses=linked_courses,
        linked_exams=linked_exams,
        saved_career_ids=saved_career_ids,
        total_careers=len(careers)
    )


# ============================================================================
# 3. Career Dossier (Full Comprehensive Profile View)
# ============================================================================

@career.route("/<slug>")
def career_detail(slug):
    career_data = Career.query.filter_by(slug=slug).first()
    if career_data is None:
        abort(404)

    # 1. Related careers in same sector
    related = Career.query.filter(
        Career.category == career_data.category,
        Career.id != career_data.id
    ).order_by(func.random()).limit(3).all()

    # 2. Relational Courses Traversal (Career -> Course -> CollegeCourse -> College)
    career_course_records = (
        CareerCourse.query.filter_by(career_id=career_data.id)
        .order_by(CareerCourse.relationship_type.asc())
        .all()
    )
    
    courses_with_colleges = []
    for cc in career_course_records:
        course = cc.course
        if course:
            # Query top 3 colleges offering this course
            offering_colleges = (
                College.query.join(CollegeCourse, College.id == CollegeCourse.college_id)
                .filter(CollegeCourse.course_id == course.id)
                .order_by(College.nirf_rank.asc().nullslast(), College.name.asc())
                .limit(3)
                .all()
            )
            total_colleges_count = (
                CollegeCourse.query.filter_by(course_id=course.id).count()
            )
            courses_with_colleges.append({
                "relation": cc,
                "course": course,
                "colleges": offering_colleges,
                "total_colleges_count": total_colleges_count
            })

    # 3. Relational Exams
    career_exam_records = (
        CareerExam.query.filter_by(career_id=career_data.id)
        .order_by(CareerExam.importance.asc())
        .all()
    )

    # 4. Structured Skills Grouping
    skills_records = CareerSkill.query.filter_by(career_id=career_data.id).all()
    grouped_skills = {
        "Technical": [],
        "Soft Skill": [],
        "Tool / Technology": []
    }
    for s in skills_records:
        cat = s.skill_category or "Technical"
        if cat not in grouped_skills:
            grouped_skills[cat] = []
        grouped_skills[cat].append(s)

    # Fallback to comma separated if skills_records empty
    if not skills_records:
        for t in career_data.technical_skills_list:
            grouped_skills["Technical"].append({"skill_name": t, "importance": "Core"})
        for sf in career_data.soft_skills_list:
            grouped_skills["Soft Skill"].append({"skill_name": sf, "importance": "Important"})
        for tl in career_data.tools_list:
            grouped_skills["Tool / Technology"].append({"skill_name": tl, "importance": "Preferred"})

    # 5. Roadmaps (Multi-route & Starting Point)
    roadmaps_all = CareerRoadmap.query.filter_by(career_id=career_data.id).all()
    routes_roadmaps = [r for r in roadmaps_all if r.path_type != "Starting Point" or not r.starting_point]
    starting_point_roadmaps = {r.starting_point: r for r in roadmaps_all if r.starting_point}

    # 6. Parse structured progressions & routes
    progression_ladder = career_data.parsed_career_progression
    entry_routes = career_data.parsed_entry_routes

    # 7. Dynamic student skill gap analysis
    user_skills = []
    if session.get("user_id"):
        user_id = session["user_id"]
        resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.created_at.desc()).first()
        if resume and resume.extracted_text:
            user_skills.extend([s.strip() for s in resume.extracted_text.split(",") if len(s.strip()) > 1])
        profile = StudentProfile.query.filter_by(user_id=user_id).first()
        if profile and profile.strengths:
            user_skills.extend([s.strip() for s in profile.strengths.split(",") if len(s.strip()) > 1])

    career_dict = {
        "title": career_data.title,
        "skills": {
            "technical": career_data.technical_skills_list
        }
    }
    gap = analyze_skill_gap(career_dict, user_skills)

    # 8. Saved status
    is_saved = False
    if session.get("user_id"):
        is_saved = SavedCareer.query.filter_by(
            user_id=session["user_id"],
            career_id=career_data.id
        ).first() is not None

    return render_template(
        "career/details.html",
        career=career_data,
        related=related,
        courses_with_colleges=courses_with_colleges,
        career_exams=career_exam_records,
        grouped_skills=grouped_skills,
        routes_roadmaps=routes_roadmaps,
        starting_point_roadmaps=starting_point_roadmaps,
        progression_ladder=progression_ladder,
        entry_routes=entry_routes,
        gap=gap,
        is_saved=is_saved,
        user_skills=user_skills
    )


# ============================================================================
# 4. "Help Me Discover Careers" (Interactive Guided Questionnaire)
# ============================================================================

@career.route("/discover", methods=["GET", "POST"])
def discover_careers():
    if request.method == "POST":
        current_status = request.form.get("current_status", "Class 12")
        stream = request.form.get("stream", "Any")
        math_interest = request.form.get("math_affinity", "3")
        tech_interest = request.form.get("tech_affinity", "3")
        creative_interest = request.form.get("creative_affinity", "3")
        people_interest = request.form.get("people_affinity", "3")
        outdoor_interest = request.form.get("outdoor_affinity", "3")
        work_mode_pref = request.form.get("work_mode_pref", "")
        preferred_orientation = request.form.get("preferred_orientation", "Balanced")

        user_input = {
            "current_level": current_status,
            "stream": stream,
            "math_affinity": math_interest,
            "tech_affinity": tech_interest,
            "creative_affinity": creative_interest,
            "people_affinity": people_interest,
            "outdoor_affinity": outdoor_interest,
            "work_mode_pref": work_mode_pref,
            "preferred_orientation": preferred_orientation
        }

        # Score every career
        all_careers = Career.query.all()
        scored_careers = []
        for c in all_careers:
            fit_result = calculate_career_fit(c, user_input)
            
            # Boost score based on orientation
            if preferred_orientation == "Public Service" and c.government_opportunities:
                fit_result["fit_score"] = min(98, fit_result["fit_score"] + 10)
            elif preferred_orientation == "High Tech & Innovation" and "technology" in c.category.lower():
                fit_result["fit_score"] = min(98, fit_result["fit_score"] + 10)
            elif preferred_orientation == "Creative & Media" and any(k in c.category.lower() for k in ["design", "media"]):
                fit_result["fit_score"] = min(98, fit_result["fit_score"] + 10)

            scored_careers.append({
                "career": c,
                "fit": fit_result
            })

        # Sort descending by fit score
        scored_careers.sort(key=lambda x: x["fit"]["fit_score"], reverse=True)
        top_matches = scored_careers[:9]

        return render_template(
            "career/discover.html",
            submitted=True,
            user_input=user_input,
            top_matches=top_matches
        )

    return render_template("career/discover.html", submitted=False)


# ============================================================================
# 5. Reverse Discovery: Degree / Course -> Career
# ============================================================================

@career.route("/explore-by-course")
def explore_by_course():
    selected_course_id = request.args.get("course_id", type=int)
    all_courses = Course.query.order_by(Course.level.asc(), Course.name.asc()).all()

    selected_course = None
    careers_linked = []

    if selected_course_id:
        selected_course = Course.query.get(selected_course_id)
        if selected_course:
            # Query careers linked through CareerCourse
            relations = (
                CareerCourse.query.filter_by(course_id=selected_course_id)
                .order_by(CareerCourse.relationship_type.asc())
                .all()
            )
            for r in relations:
                if r.career:
                    careers_linked.append({
                        "career": r.career,
                        "relationship_type": r.relationship_type,
                        "description": r.description
                    })

    return render_template(
        "career/explore_by_course.html",
        courses=all_courses,
        selected_course=selected_course,
        careers_linked=careers_linked
    )


# ============================================================================
# 6. Reverse Discovery: Skills -> Career
# ============================================================================

@career.route("/explore-by-skills")
def explore_by_skills():
    selected_skill = request.args.get("skill", "").strip()

    # Top popular skills from career_skills
    popular_skills_raw = (
        db.session.query(CareerSkill.skill_name, func.count(CareerSkill.career_id))
        .group_by(CareerSkill.skill_name)
        .order_by(func.count(CareerSkill.career_id).desc())
        .limit(30)
        .all()
    )
    popular_skills = [r[0] for r in popular_skills_raw]

    matching_careers = []
    if selected_skill:
        # Search careers requiring this skill
        matching_skill_records = (
            CareerSkill.query.filter(CareerSkill.skill_name.ilike(f"%{selected_skill}%"))
            .all()
        )
        career_ids = list({s.career_id for s in matching_skill_records})
        if career_ids:
            matching_careers = Career.query.filter(Career.id.in_(career_ids)).order_by(Career.title.asc()).all()
        else:
            matching_careers = Career.query.filter(Career.technical_skills.ilike(f"%{selected_skill}%")).all()

    return render_template(
        "career/explore_by_skills.html",
        popular_skills=popular_skills,
        selected_skill=selected_skill,
        matching_careers=matching_careers
    )


# ============================================================================
# 7. Reverse Discovery: School / College Subject -> Career
# ============================================================================

@career.route("/explore-by-subject")
def explore_by_subject():
    SUBJECTS = [
        {"name": "Mathematics", "icon": "calculator", "desc": "Calculus, algebra, statistics, discrete maths"},
        {"name": "Physics", "icon": "lightning-charge", "desc": "Mechanics, electronics, optics, thermodynamics"},
        {"name": "Chemistry", "icon": "droplet-half", "desc": "Organic, physical, industrial chemistry & biochemistry"},
        {"name": "Biology", "icon": "heart-pulse", "desc": "Genetics, human physiology, ecology, pathology"},
        {"name": "Computer Science", "icon": "code-slash", "desc": "Programming, algorithms, web technologies"},
        {"name": "Economics", "icon": "graph-up", "desc": "Macro, micro, public policy, econometric analysis"},
        {"name": "Accountancy", "icon": "journal-bookmark", "desc": "Financial reporting, taxation, auditing"},
        {"name": "Political Science", "icon": "bank", "desc": "Constitution, governance, international relations"},
        {"name": "History", "icon": "hourglass-split", "desc": "Historical civilizations, heritage, public policy"},
        {"name": "Psychology", "icon": "person-heart", "desc": "Human behavior, cognitive sciences, mental wellness"},
        {"name": "Fine Arts & Design", "icon": "palette", "desc": "Visual aesthetics, sketching, 3D modeling"},
        {"name": "English & Literature", "icon": "book", "desc": "Written communications, journalism, public relations"}
    ]

    selected_subject = request.args.get("subject", "").strip()
    matching_careers = []

    if selected_subject:
        matching_careers = Career.query.filter(
            or_(
                Career.required_subjects.ilike(f"%{selected_subject}%"),
                Career.technical_skills.ilike(f"%{selected_subject}%"),
                Career.preferred_streams.ilike(f"%{selected_subject}%"),
                Career.description.ilike(f"%{selected_subject}%")
            )
        ).order_by(Career.title.asc()).all()

    return render_template(
        "career/explore_by_subject.html",
        subjects=SUBJECTS,
        selected_subject=selected_subject,
        matching_careers=matching_careers
    )


# ============================================================================
# 8. Compare Careers (Up to 4 careers side-by-side)
# ============================================================================

@career.route("/compare")
def compare():
    slugs = [
        request.args.get("career1", "").strip(),
        request.args.get("career2", "").strip(),
        request.args.get("career3", "").strip(),
        request.args.get("career4", "").strip()
    ]
    active_slugs = [s for s in slugs if s]

    all_careers = Career.query.order_by(Career.title.asc()).all()

    if len(active_slugs) < 2:
        return render_template(
            "career/compare_select.html",
            careers=all_careers,
            selected_slugs=active_slugs
        )

    compared_careers = []
    for s in active_slugs:
        c = Career.query.filter_by(slug=s).first()
        if c:
            compared_careers.append(c)

    if len(compared_careers) < 2:
        flash("Please select at least 2 valid careers to compare.", "warning")
        return render_template(
            "career/compare_select.html",
            careers=all_careers,
            selected_slugs=active_slugs
        )

    return render_template(
        "career/compare.html",
        careers=compared_careers,
        all_careers=all_careers
    )


# ============================================================================
# 9. Interactive Career Fit Calculator API Endpoint
# ============================================================================

@career.route("/api/fit-calculator", methods=["POST"])
def api_fit_calculator():
    data = request.get_json() or {}
    career_id = data.get("career_id")
    career_obj = Career.query.get(career_id)

    if not career_obj:
        return jsonify({"error": "Career not found"}), 404

    fit_result = calculate_career_fit(career_obj, data)
    return jsonify(fit_result)


# ============================================================================
# 10. AI Career Counsellor Query API Endpoint (Grounded in DB Facts)
# ============================================================================

@career.route("/api/counsellor", methods=["POST"])
def api_counsellor():
    data = request.get_json() or {}
    query_text = data.get("query", "").strip()
    career_slug = data.get("career_slug")

    if not query_text:
        return jsonify({"error": "Query cannot be empty"}), 400

    response_text = generate_counsellor_response(query_text, career_slug)
    return jsonify({
        "success": True,
        "response": response_text
    })


# ============================================================================
# 11. Save / Bookmark Career Toggle
# ============================================================================

@career.route("/save/<int:career_id>")
def toggle_save(career_id):
    if "user_id" not in session:
        flash("Please log in to save careers to your profile.", "info")
        return redirect(url_for("auth.login"))

    career_obj = Career.query.get_or_404(career_id)

    existing = SavedCareer.query.filter_by(
        user_id=session["user_id"],
        career_id=career_id
    ).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f"{career_obj.title} removed from saved careers.", "info")
    else:
        saved = SavedCareer(
            user_id=session["user_id"],
            career_id=career_id
        )
        db.session.add(saved)
        db.session.commit()
        flash(f"{career_obj.title} saved to your profile!", "success")

    return redirect(request.referrer or url_for("career.career_detail", slug=career_obj.slug))


# ============================================================================
# 12. Non-Biased Career Discovery Gateways
# ============================================================================

@career.route("/without-coding")
def careers_without_coding():
    """
    Discovery pathway for students seeking rewarding non-coding, non-IT careers.
    Highlights Law, Healthcare, Design, Civil Services, Finance, Education, Psychology, etc.
    """
    page = request.args.get("page", 1, type=int)
    category = request.args.get("category", "").strip()
    stream = request.args.get("stream", "").strip()
    per_page = 16

    query = Career.query.filter(
        ~Career.category.in_(["Technology & Computer Science"]),
        ~Career.sub_category.ilike("%Software%"),
        ~Career.sub_category.ilike("%Computer%"),
        ~Career.technical_skills.ilike("%Python%"),
        ~Career.technical_skills.ilike("%Java%"),
        ~Career.technical_skills.ilike("%C++%"),
        ~Career.technical_skills.ilike("%Coding%")
    )

    if category:
        query = query.filter(Career.category == category)
    if stream:
        query = query.filter(
            or_(
                Career.preferred_streams.ilike(f"%{stream}%"),
                Career.preferred_streams.ilike("%any%"),
                Career.preferred_streams.ilike("%open%")
            )
        )

    pagination = query.order_by(Career.title.asc()).paginate(page=page, per_page=per_page, error_out=False)
    
    categories = (
        db.session.query(Career.category, func.count(Career.id))
        .filter(
            ~Career.category.in_(["Technology & Computer Science"]),
            ~Career.sub_category.ilike("%Software%"),
            ~Career.technical_skills.ilike("%Python%")
        )
        .group_by(Career.category)
        .all()
    )

    return render_template(
        "career/without_coding.html",
        careers=pagination.items,
        pagination=pagination,
        categories=categories,
        selected_category=category,
        selected_stream=stream,
        total_count=pagination.total
    )


@career.route("/without-engineering")
def careers_without_engineering():
    """
    Discovery pathway for students who do not wish to pursue B.Tech/Engineering degrees.
    Shows Medicine, Law, Management, Civil Services, Arts, Agriculture, Media, Social Sciences, etc.
    """
    page = request.args.get("page", 1, type=int)
    category = request.args.get("category", "").strip()
    stream = request.args.get("stream", "").strip()
    per_page = 16

    query = Career.query.filter(
        ~Career.category.in_(["Engineering & Manufacturing", "Technology & Computer Science"]),
        ~Career.minimum_qualification.ilike("%B.Tech%"),
        ~Career.minimum_qualification.ilike("%B.E.%")
    )

    if category:
        query = query.filter(Career.category == category)
    if stream:
        query = query.filter(
            or_(
                Career.preferred_streams.ilike(f"%{stream}%"),
                Career.preferred_streams.ilike("%any%"),
                Career.preferred_streams.ilike("%open%")
            )
        )

    pagination = query.order_by(Career.title.asc()).paginate(page=page, per_page=per_page, error_out=False)

    categories = (
        db.session.query(Career.category, func.count(Career.id))
        .filter(
            ~Career.category.in_(["Engineering & Manufacturing", "Technology & Computer Science"]),
            ~Career.minimum_qualification.ilike("%B.Tech%"),
            ~Career.minimum_qualification.ilike("%B.E.%")
        )
        .group_by(Career.category)
        .all()
    )

    return render_template(
        "career/without_engineering.html",
        careers=pagination.items,
        pagination=pagination,
        categories=categories,
        selected_category=category,
        selected_stream=stream,
        total_count=pagination.total
    )


@career.route("/lesser-known")
def lesser_known_careers():
    """
    Section: 'Careers You May Not Know About' / 'I Never Knew This Was A Career'
    High-value, specialized, and unique occupations across Science, Allied Health, Design, Law, etc.
    """
    page = request.args.get("page", 1, type=int)
    category = request.args.get("category", "").strip()
    per_page = 16

    query = Career.query.filter(Career.is_lesser_known == True)
    if category:
        query = query.filter(Career.category == category)

    pagination = query.order_by(Career.title.asc()).paginate(page=page, per_page=per_page, error_out=False)

    categories = (
        db.session.query(Career.category, func.count(Career.id))
        .filter(Career.is_lesser_known == True)
        .group_by(Career.category)
        .all()
    )

    return render_template(
        "career/lesser_known.html",
        careers=pagination.items,
        pagination=pagination,
        categories=categories,
        selected_category=category,
        total_count=pagination.total
    )


@career.route("/no-idea")
def no_idea():
    """
    'I Don't Know What Career I Want' - Guided Self-Discovery Explorer.
    Students are NOT forced to pick an industry or degree. Instead they answer
    questions about preferences, activities, working styles, and affinity.
    """
    all_clusters = [
        {"name": "People & Society", "icon": "people", "desc": "Interacting with individuals, counselling, community welfare, public administration"},
        {"name": "Numbers & Analysis", "icon": "calculator", "desc": "Financial models, statistics, risk calculation, budgeting, quantitative analysis"},
        {"name": "Science & Medicine", "icon": "heart-pulse", "desc": "Healthcare, laboratory diagnostics, clinical trials, pathology, biology"},
        {"name": "Nature & Agriculture", "icon": "tree", "desc": "Crops, wildlife conservation, forestry, soil science, environmental sustainability"},
        {"name": "Writing & Languages", "icon": "pen", "desc": "Journalism, literature, content editing, linguistics, creative writing, translation"},
        {"name": "Creative Arts & Design", "icon": "palette", "desc": "UI/UX, visual styling, fashion, 3D modelling, architecture, fine arts"},
        {"name": "Law, Justice & Policy", "icon": "bank", "desc": "Judicial advocacy, legal contracts, human rights, governance policy, regulation"},
        {"name": "Uniformed & Leadership", "icon": "shield-check", "desc": "Armed forces, police administration, emergency services, crisis commanding"},
        {"name": "Teaching & Pedagogy", "icon": "mortarboard", "desc": "Classroom instruction, academic research, student mentoring, curriculum design"},
        {"name": "Hands-On & Technical", "icon": "tools", "desc": "Vocational trades, machinery, physical fabrication, electrical systems, operations"},
        {"name": "Sports & Movement", "icon": "trophy", "desc": "Athletic coaching, physiotherapy, fitness training, performance analytics"},
        {"name": "Travel & Hospitality", "icon": "compass", "desc": "Culinary arts, hotel management, aviation operations, international tourism"}
    ]
    return render_template("career/no_idea.html", clusters=all_clusters)


@career.route("/interest-clusters")
def interest_clusters():
    """
    Multi-dimensional exploration organized by Career Interest Clusters.
    """
    cluster = request.args.get("cluster", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 16

    query = Career.query
    if cluster:
        query = query.filter(Career.interest_clusters.ilike(f"%{cluster}%"))

    pagination = query.order_by(Career.title.asc()).paginate(page=page, per_page=per_page, error_out=False)

    clusters_list = [
        "People", "Numbers", "Science", "Nature", "Animals", "Language",
        "Writing", "Creativity", "Art", "Business", "Leadership", "Helping",
        "Law", "Government", "Research", "Teaching", "Healthcare", "Sports",
        "Travel", "Hands-on work", "Machines", "Design", "Media", "Society"
    ]

    return render_template(
        "career/interest_clusters.html",
        careers=pagination.items,
        pagination=pagination,
        selected_cluster=cluster,
        clusters=clusters_list,
        total_count=pagination.total
    )


@career.route("/work-styles")
def work_styles():
    """
    Explore careers organized by physical Work Style and Workplace Environment.
    (Hospital, Court, Office, Outdoor, Laboratory, Studio, Field, School, Workshop, Remote, Travel)
    """
    style = request.args.get("style", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 16

    query = Career.query
    if style:
        query = query.filter(Career.work_style.ilike(f"%{style}%"))

    pagination = query.order_by(Career.title.asc()).paginate(page=page, per_page=per_page, error_out=False)

    styles_list = [
        {"id": "Hospital", "label": "Hospital & Clinical", "icon": "hospital"},
        {"id": "Court", "label": "Court & Legal Chambers", "icon": "bank"},
        {"id": "Government Office", "label": "Government & Civil Secretariat", "icon": "building"},
        {"id": "School", "label": "School & University Campus", "icon": "mortarboard"},
        {"id": "Laboratory", "label": "Scientific Laboratory", "icon": "eyedropper"},
        {"id": "Field", "label": "Field Work & Community", "icon": "geo-alt"},
        {"id": "Outdoor", "label": "Outdoors & Nature / Farm", "icon": "tree"},
        {"id": "Studio", "label": "Design & Media Studio", "icon": "palette"},
        {"id": "Workshop", "label": "Industrial Workshop / Trade", "icon": "tools"},
        {"id": "Office", "label": "Corporate / Professional Office", "icon": "briefcase"},
        {"id": "Travel", "label": "Travel & Aviation / Maritime", "icon": "airplane"},
        {"id": "Remote", "label": "Remote / Hybrid Eligible", "icon": "laptop"}
    ]

    return render_template(
        "career/work_styles.html",
        careers=pagination.items,
        pagination=pagination,
        selected_style=style,
        styles=styles_list,
        total_count=pagination.total
    )