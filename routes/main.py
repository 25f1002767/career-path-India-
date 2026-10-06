from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    jsonify
)
from sqlalchemy import or_

from models.career import Career
from models.college import College
from models.course import Course
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship

main = Blueprint(
    "main",
    __name__
)


def get_home_context():
    """
    Retrieves real, comprehensive database metrics and featured records
    for the MPath national career discovery experience.
    """
    career_count = Career.query.count()
    college_count = College.query.count()
    course_count = Course.query.count()
    exam_count = GovernmentExam.query.count()
    scholarship_count = Scholarship.query.count()
    internship_count = Internship.query.count()

    counts = {
        "careers": career_count,
        "colleges": college_count,
        "courses": course_count,
        "exams": exam_count,
        "scholarships": scholarship_count,
        "internships": internship_count,
        "opportunities": scholarship_count + internship_count
    }

    # Featured careers across key national tracks
    featured_careers = Career.query.filter(
        Career.title.in_([
            "Software Developer",
            "General Physician / Medical Doctor",
            "Data Scientist",
            "Civil Services / IAS Officer",
            "Chartered Accountant (CA)",
            "Aerospace Engineer",
            "Corporate Lawyer",
            "Psychologist / Mental Health Professional"
        ])
    ).limit(8).all()
    if len(featured_careers) < 4:
        featured_careers = Career.query.limit(8).all()

    # Top premier institutions with NIRF ranks
    featured_colleges = College.query.filter(
        College.nirf_rank.isnot(None)
    ).order_by(College.nirf_rank.asc()).limit(6).all()
    if not featured_colleges:
        featured_colleges = College.query.limit(6).all()

    # Major Government Examinations
    featured_exams = GovernmentExam.query.limit(6).all()

    # Verified Scholarships
    featured_scholarships = Scholarship.query.limit(6).all()

    # Verified AICTE Internships
    featured_internships = Internship.query.limit(6).all()

    # Popular Undergraduate & Postgraduate Degree Programs
    featured_courses = Course.query.limit(8).all()

    return {
        "counts": counts,
        "featured_careers": featured_careers,
        "featured_colleges": featured_colleges,
        "featured_exams": featured_exams,
        "featured_scholarships": featured_scholarships,
        "featured_internships": featured_internships,
        "featured_courses": featured_courses,
    }


@main.route("/")
def index():
    return render_template("home/hero.html", **get_home_context())


@main.route("/dashboard")
def dashboard():
    return redirect(url_for("dashboard.home"))


@main.route("/ai-mentor")
def ai_mentor():
    return redirect(url_for("chatbot.home"))


@main.route("/api/quick-search")
def quick_search():
    """
    Live real-time search suggestions connecting to genuine database records.
    Returns categorized entries for Careers, Courses, Colleges, Exams, Scholarships.
    """
    query = request.args.get("q", "").strip()
    if not query or len(query) < 2:
        return jsonify({"results": []})

    pattern = f"%{query}%"
    results = []

    # 1. Careers
    careers = Career.query.filter(
        or_(
            Career.title.ilike(pattern),
            Career.category.ilike(pattern),
            Career.sub_category.ilike(pattern)
        )
    ).limit(4).all()
    for c in careers:
        results.append({
            "title": c.title,
            "category": "CAREER",
            "subtitle": c.category or "Career Pathway",
            "url": url_for("career.career_detail", slug=c.slug or c.id),
            "icon": "briefcase"
        })

    # 2. Courses
    courses = Course.query.filter(
        or_(
            Course.name.ilike(pattern),
            Course.short_name.ilike(pattern),
            Course.discipline.ilike(pattern)
        )
    ).limit(4).all()
    for co in courses:
        results.append({
            "title": co.name,
            "category": "COURSE",
            "subtitle": f"{co.level or 'Degree'} | {co.discipline or 'Discipline'}",
            "url": url_for("course.course_detail", course_id=co.id),
            "icon": "book-open"
        })

    # 3. Colleges
    colleges = College.query.filter(
        or_(
            College.name.ilike(pattern),
            College.short_name.ilike(pattern),
            College.city.ilike(pattern),
            College.course.ilike(pattern)
        )
    ).limit(4).all()
    for col in colleges:
        loc = f"{col.city}, {col.state}" if col.city and col.state else col.city or col.state or ""
        nirf = f" | NIRF #{col.nirf_rank}" if col.nirf_rank else ""
        results.append({
            "title": col.name,
            "category": "COLLEGE",
            "subtitle": f"{col.display_type}{nirf} | {loc}",
            "url": url_for("college.college_detail", college_id=col.id),
            "icon": "landmark"
        })

    # 4. Government Exams
    exams = GovernmentExam.query.filter(
        or_(
            GovernmentExam.exam_name.ilike(pattern),
            GovernmentExam.category.ilike(pattern)
        )
    ).limit(3).all()
    for e in exams:
        results.append({
            "title": e.exam_name,
            "category": "EXAM",
            "subtitle": f"{e.category or 'Government Exam'} | {e.conducting_body or ''}",
            "url": url_for("exam.exam_detail", exam_id=e.id),
            "icon": "file-text"
        })

    # 5. Verified Scholarships
    scholarships = Scholarship.query.filter(
        or_(
            Scholarship.title.ilike(pattern),
            Scholarship.provider.ilike(pattern),
            Scholarship.category.ilike(pattern)
        )
    ).limit(3).all()
    for s in scholarships:
        results.append({
            "title": s.title,
            "category": "SCHOLARSHIP",
            "subtitle": s.provider or "National Scholarship",
            "url": url_for("scholarship.scholarship_detail", identifier=s.slug or s.id),
            "icon": "award"
        })

    return jsonify({"results": results[:12]})


@main.route("/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("search/results.html", query="", total_results=0)

    pattern = f"%{query}%"

    careers = Career.query.filter(
        or_(
            Career.title.ilike(pattern),
            Career.category.ilike(pattern),
            Career.description.ilike(pattern),
            Career.skills_required.ilike(pattern)
        )
    ).limit(8).all()

    colleges = College.query.filter(
        or_(
            College.name.ilike(pattern),
            College.city.ilike(pattern),
            College.state.ilike(pattern),
            College.course.ilike(pattern)
        )
    ).limit(8).all()

    exams = GovernmentExam.query.filter(
        or_(
            GovernmentExam.exam_name.ilike(pattern),
            GovernmentExam.category.ilike(pattern),
            GovernmentExam.description.ilike(pattern)
        )
    ).limit(8).all()

    scholarships = Scholarship.query.filter(
        or_(
            Scholarship.title.ilike(pattern),
            Scholarship.provider.ilike(pattern),
            Scholarship.category.ilike(pattern)
        )
    ).limit(8).all()

    internships = Internship.query.filter(
        or_(
            Internship.title.ilike(pattern),
            Internship.company.ilike(pattern),
            Internship.skills.ilike(pattern),
            Internship.domain.ilike(pattern)
        )
    ).limit(8).all()

    total_results = len(careers) + len(colleges) + len(exams) + len(scholarships) + len(internships)

    return render_template(
        "search/results.html",
        query=query,
        careers=careers,
        colleges=colleges,
        exams=exams,
        scholarships=scholarships,
        internships=internships,
        total_results=total_results
    )